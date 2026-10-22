# 11 — INTEGRATION GUIDE
**Projeto AURA · v1.0.0**
Como consumir o pack em engines reais. Cobre o formato skeletal (preferido), o baked (fallback), o contrato de dados, o state machine de animação e exemplos em web, Godot e Unity.

---

## 1. Contrato de dados

O pack entrega quatro coisas, e só elas são normativas:

1. **Partes** — PNG RGBA com pivô (`parts/*.png` + `rig.json`).
2. **Esqueleto** — hierarquia, rest pose, limites (`skeleton.json`).
3. **Clipes** — keyframes, curvas, eventos (`animations/*.json`).
4. **Metadados** — IDs, sockets, hurtbox, compatibilidade (`*.json`).

Nada no pack depende de uma engine. Os exemplos abaixo são **implementações de referência**, não a entrega.

---

## 2. ADR-0004 — Dois caminhos de render

| Caminho | Quando usar | Custo | Fluidez |
|---|---|---|---|
| **Skeletal** (recomendado) | PC, mobile moderno, web com canvas/WebGL | baixo (1 atlas por personagem) | 60 fps real, blend contínuo |
| **Baked** | engines simples, pixel-perfect determinístico, replay | alto (N frames × clipes) | 30–60 fps, sem blend entre clipes |

- O mesmo rig gera os dois. Nunca há divergência de arte.
- O pack declara `render_modes: ["skeletal", "baked"]` no metadata.
- Preview GIF usa o caminho skeletal renderizado off-line.

---

## 3. Pipeline de transformação (referência)

Para cada frame, para cada osso:

```
world = parent.world × T(rest_pos) × R(local_rot) × S(local_scale)
```

- `rest_pos` em world px (doc 03 §3).
- `local_rot` = `rest_angle + track_value` (graus → radianos).
- O pivô do attachment é subtraído no desenho: `draw_pos = world_pos − pivot`.
- Ordem de desenho: `layer_order.json` (crescente).
- Espelhamento: aplicar `scaleX = −1` no actor e espelhar sockets e VFX.

Pseudocódigo:

```python
def pose_at(clip, t):                  # t em frames (float, 60 fps)
    pose = {}
    for bone, tracks in clip.tracks.items():
        pose[bone] = {
            "rot": sample(tracks.get("rotation", []), t, default=0),
            "pos": sample(tracks.get("position", []), t, default=[0, 0]),
            "scale": sample(tracks.get("scale", []), t, default=[1, 1]),
        }
    return pose

def world_matrix(skeleton, pose, bone):
    b = skeleton[bone]
    local = T(b.rest_pos + pose[bone]["pos"]) @ R(pose[bone]["rot"]) @ S(pose[bone]["scale"])
    return world_matrix(skeleton, pose, b.parent) @ local if b.parent else local
```

---

## 4. State machine de animação

```
                 ┌──────────► hurt ──► death
                 │              │
 idle ◄──► walk ◄─┼──► run       └──► idle
   │         │    │
   └──► attack ┴──► cast ──► idle
          │
          └──► dodge / block
```

Regras:
- Prioridade: `death > hurt > dodge > attack > cast > run > walk > idle`.
- `hurt` cancela qualquer coisa (blend 0).
- Ataque só cancela após `cancel` (doc 04 §5).
- Combo só dentro de `combo_window`.
- Estado `dead` não sai sem `revive`.
- Troca de clipe usa blend de pose (doc 04 §9), não cross-fade de textura.

### 4.1 Implementação mínima
```js
const PRIORITY = { death: 100, hurt: 90, dodge: 80, attack: 70, cast: 60, run: 30, walk: 20, idle: 10 };

function requestClip(name, opts = {}) {
  const cur = state.clip;
  if (!opts.force && PRIORITY[name] < PRIORITY[cur]) return false;
  if (cur && !canCancel(cur, state.time)) return false;
  state.prev = cur ? samplePose(cur, state.time) : null;
  state.clip = name;
  state.time = 0;
  state.blend = opts.blend ?? 0.12;   // segundos
  return true;
}
```

---

## 5. Eventos

- O runtime dispara eventos ao **cruzar** o frame do evento, nunca a cada frame.
- `hit_frame` → aplica dano; `vfx_emit` → instancia efeito no socket; `shake` → câmera.
- Eventos são suprimidos durante blend do clipe de origem.
- Em hitstop, o tempo do clipe congela, mas a câmera e os VFX continuam.

```js
function update(dt) {
  state.time += dt * state.speed;
  eventsBetween(state.clip, state.prevTime, state.time).forEach(dispatch);
  state.prevTime = state.time;
}
```

---

## 6. IK de perna (foot planting)

Alvo do pé em world space; resolve 2 ossos (coxa/canela) por lei dos cossenos:

```python
def ik2(hip, target, l1, l2, bend=+1):
    d = clamp(dist(hip, target), abs(l1 - l2) + 1e-3, l1 + l2 - 1e-3)
    a = acos((l1*l1 + d*d - l2*l2) / (2*l1*d))
    base = atan2(target.y - hip.y, target.x - hip.x)
    knee = hip + vec(cos(base + bend*a), sin(base + bend*a)) * l1
    return knee, target
```

- Durante a fase de apoio, `target` fica **fixo** no mundo.
- Durante o balanço, `target` segue a curva do clipe.
- Tornozelo recebe o ângulo para manter a sola paralela ao chão.
- Se o alvo estiver fora de alcance, a perna estica (nunca “quebra”).

---

## 7. Secundárias (spring)

```python
class Spring:
    def __init__(self, k, c, limit):
        self.k, self.c, self.limit = k, c, limit
        self.theta, self.omega = 0.0, 0.0

    def update(self, target, dt):
        a = -self.k * (self.theta - target) - self.c * self.omega
        self.omega += a * dt
        self.theta += self.omega * dt
        self.theta = max(-self.limit, min(self.limit, self.theta))
        return self.theta
```

- Um spring por osso da cadeia, com o alvo do filho derivado do pai.
- Integrar a passo fixo (60 Hz) para determinismo.
- Parâmetros em `standards/easing_library.json#springs`.

---

## 8. Web (Canvas 2D / PixiJS)

```js
class PaperDoll {
  constructor(rig, atlas, images) {
    this.rig = rig; this.atlas = atlas; this.img = images;
    this.pose = {}; this.time = 0; this.clip = null;
  }
  setClip(clip, blend = 0.12) {
    this.prev = this.clip ? this.sample() : null;
    this.clip = clip; this.time = 0; this.blend = blend;
  }
  sample() {
    const out = {};
    for (const [bone, tracks] of Object.entries(this.clip.tracks)) {
      out[bone] = {
        rot: sampleTrack(tracks.rotation, this.time, 0),
        pos: sampleTrack(tracks.position, this.time, [0, 0]),
        scale: sampleTrack(tracks.scale, this.time, [1, 1]),
      };
    }
    return out;
  }
  draw(ctx, x, y, flip = false) {
    const pose = mixPose(this.prev, this.sample(), this.blendRatio());
    const world = computeWorld(this.rig.skeleton, pose);
    ctx.save();
    ctx.translate(x, y);
    if (flip) ctx.scale(-1, 1);
    for (const slot of this.rig.slots) {
      const m = world[slot.bone];
      const part = this.atlas.frames[slot.attachment];
      ctx.save();
      ctx.translate(m.x - part.pivot[0], -m.y - part.pivot[1]);
      ctx.rotate(m.rot);
      ctx.drawImage(this.img[slot.attachment], part.x, part.y, part.w, part.h, 0, 0, part.w, part.h);
      ctx.restore();
    }
    ctx.restore();
  }
}
```

Pontos de atenção:
- `ctx.imageSmoothingEnabled = false` só se a arte for pixel-perfect; aqui usar `true`.
- Desenhar com `devicePixelRatio` para nitidez.
- Atlas único por personagem evita troca de textura.
- Em WebGL, usar sprites agrupados por textura e ordem de camada.

---

## 9. Godot 4 (GDScript)

Estrutura de cena:

```
Actor (Node2D)
├── Skeleton2D
│   └── Bone2D (root → pelvis → ...)
├── Parts (Node2D)
│   ├── Sprite2D (torso, bone="chest")
│   └── Sprite2D (...)
└── Animator (Node)
```

- Importar `rig.json` num `@tool` que cria os `Bone2D` e os `Sprite2D` com `offset` = pivô.
- Carregar `animations/*.json` em um `AnimationPlayer` construído em runtime (ou em `.tres` gerado).
- Para secundárias, `SpringArm` manual em `_process` ou `SkeletonModifier2D`.

```gdscript
func _process(delta: float) -> void:
    _time += delta * speed
    var pose := sample_clip(clip, _time)
    for bone_name in pose:
        var b: Bone2D = bones[bone_name]
        b.rotation = deg_to_rad(pose[bone_name].rot)
    for slot in slots:
        var s: Sprite2D = slot.node
        s.position = slot.offset
        s.rotation = bones[slot.bone].global_rotation
```

Dicas:
- Use `CanvasItem.z_index` conforme `layer_order.json` × 10.
- `texture_filter = TEXTURE_FILTER_LINEAR_WITH_MIPMAPS` e atlas com padding.
- Para 30+ atores, considere `MultiMeshInstance2D` ou baked sheets.

---

## 10. Unity (C#)

```csharp
public class PaperDoll : MonoBehaviour {
    public RigData rig;           // ScriptableObject gerado do JSON
    public SpriteAtlas atlas;
    Transform[] bones; SpriteRenderer[] parts;

    void LateUpdate() {
        var pose = ClipSampler.Sample(rig, current, time);
        for (int i = 0; i < bones.Length; i++) {
            var b = rig.skeleton[i];
            bones[i].localPosition = b.restPos + pose[b.name].pos;
            bones[i].localRotation = Quaternion.Euler(0, 0, pose[b.name].rot);
            bones[i].localScale = pose[b.name].scale;
        }
        for (int i = 0; i < parts.Length; i++)
            parts[i].sortingOrder = rig.slots[i].layer * 10;
    }
}
```

- Um `SpriteRenderer` por slot, filho do osso correspondente, `sprite.pivot` = pivô do PNG.
- `sortingOrder` por camada evita z-fighting.
- Para muitos atores, use `SpriteSkin`/`2D Animation` package ou o caminho baked.

---

## 11. Jogo: o que liga na animação

| Sistema | Contrato com o pack |
|---|---|
| Movimento | velocidade 140/340 px/s; fase da animação sincronizada com distância percorrida |
| Facing | `+X` por padrão; espelhar em `−X` |
| Combate | hit frame do clipe define o instante do dano; `cancel` define input buffer |
| Dano | hitstop 3/5/8 frames; flash; knockback 6/18/28 px |
| Alvo | retângulo/elipse do hurtbox do alvo; auto-attack a 2 s |
| Skills | 5 slots + auto-attack (1º slot) |
| Câmera | shake por evento; zoom fixo; seguir ator com deadzone |
| Depth | ordenar por `foot_y`; escala 1,00→0,86 na faixa de chão |
| Rede | servidor autoritativo; cliente prediz animação e posição |

---

## 12. Carregamento e performance

- Baixar **1 atlas por personagem** + 1 JSON de rig + N clipes.
- Pré-carregar clipes usados em combate; streaming para emotes.
- Cache de textura por `asset_id@version`.
- Limite: 30 personagens → ≤ 30 atlas de 2048² (≈ 480 MB de VRAM) — usar atlas de 1024² e compressão (ASTC/ETC2) em mobile.
- Baked sheets só para inimigos numerosos.

---

## 13. Depuração

Overlay de debug (obrigatório nos exemplos):
- ossos desenhados;
- pivôs;
- hurtbox/hitbox;
- socket de arma;
- nome do clipe + frame;
- eventos disparados no frame;
- contador de draw calls.

---

## 14. Critérios de integração aceitos

- [ ] Personagem montado só com arquivos do pack.
- [ ] Idle, walk, run, attack e hurt executando com eventos.
- [ ] Troca de arma em runtime sem recarregar rig.
- [ ] Espelhamento sem artefato.
- [ ] 30 atores a 60 fps na cena de teste.
- [ ] HUD montada com o kit e sem texto embutido.
- [ ] Mapa com colisão, portal e oclusão funcionando.
