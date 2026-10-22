# 10 — NAMING E METADADOS
**Projeto AURA · v1.0.0**
Regras de identificação, nomenclatura de arquivos, schemas, manifesto e versionamento.

---

## 1. Identificadores

### 1.1 Formato

```
DB_<CATEGORY>_<SUBCATEGORY>_<NAME>_<VARIANT>_<STATE>
```

- Prefixo `DB_` fixo (master-prompt §5).
- Segmentos em **MAIÚSCULAS**, `A-Z`, `0-9` e `_` apenas.
- Sem acentos, sem espaços, sem hífen, sem camelCase.
- `VARIANT` e `STATE` são opcionais, mas quando existem ficam nessa ordem.
- Comprimento máximo: 64 caracteres.
- Regex: `^DB_[A-Z0-9]+(_[A-Z0-9]+){2,5}$`

### 1.2 Categorias

| Código | Escopo | Exemplo |
|---|---|---|
| `CHAR` | personagem jogável/NPC/vilão | `DB_CHAR_HERO_GOKU_BASE_IDLE` |
| `RIG` | esqueleto reutilizável | `DB_RIG_HUMANOID_MALE_A` |
| `EQUIP` | armadura, arma, helm, capa, etc. | `DB_EQUIP_WEAPON_SWORD_TRUNKS` |
| `ENEMY` | inimigo | `DB_ENEMY_COMMON_SAIBAMAN_GREEN` |
| `PET` | mascote/invocação | `DB_PET_PUAR_DEFAULT_FOLLOW` |
| `SKILL` | habilidade (conjunto) | `DB_SKILL_BEAM_KAMEHAMEHA_BLUE` |
| `VFX` | efeito isolado | `DB_VFX_KI_EXPLOSION_BLUE_01` |
| `ENV` | cenário/camada/prop | `DB_ENV_NAMEK_SKY_DAY` |
| `MAP` | mapa composto | `DB_MAP_EARTH_PAOZU_DAY` |
| `UI` | interface | `DB_UI_HUD_PLAYER_FRAME` |
| `ITEM` | item de inventário | `DB_ITEM_CONSUMABLE_SENZU_BEAN` |
| `ICON` | ícone | `DB_ICON_SKILL_KAMEHAMEHA` |

### 1.3 Subcategorias padronizadas

| Categoria | Subcategorias |
|---|---|
| `CHAR` | `HERO`, `VILLAIN`, `NPC`, `BASE`, `DUMMY` |
| `EQUIP` | `ARMOR`, `WEAPON`, `HELM`, `HAIR`, `CAPE`, `GLOVE`, `BOOT`, `ACC` |
| `ENEMY` | `COMMON`, `ELITE`, `BOSS` |
| `PET` | `COMPANION`, `CREATURE`, `SUMMON` |
| `SKILL` | `MELEE`, `BEAM`, `BLAST`, `BUFF`, `HEAL`, `TRANSFORM` |
| `VFX` | `SLASH`, `IMPACT`, `EXPLOSION`, `AURA`, `TRAIL`, `DUST`, `SPARK` |
| `ENV` | `SKY`, `HORIZON`, `MID`, `STRUCTURE`, `DECOR`, `GROUND`, `PROP`, `FG`, `OCCLUDER` |

### 1.4 Variantes
`BASE`, `SSJ`, `SSJ2`, `SSJ3`, `SSG`, `SSB`, `SSBE`, `UI_SIGN`, `UI`, `BEAST`, `GOLDEN`, `CC1_BLUE`, `CC2_RED`, `GREEN`, `ELITE`, `BROKEN`.
Variantes são parte da identidade: `GOKU_SSJ` ≠ `GOKU_BASE`.

### 1.5 Estados
`IDLE`, `IDLE_COMBAT`, `WALK`, `RUN`, `JUMP`, `FALL`, `LAND`, `DODGE`, `BLOCK`, `HURT_LIGHT`, `HURT_HEAVY`, `HURT_CRIT`, `KNOCKBACK`, `DEATH`, `REVIVE`, `ATTACK01..03`, `ATTACK_HEAVY`, `ATTACK_CRIT`, `ATTACK_WHIFF`, `CAST`, `CHANNEL`, `CHARGE`, `VICTORY`, `TAUNT`, `SPAWN`, `TRANSFORM_IN`, `TRANSFORM_OUT`, `ICON`, `PORTRAIT`.

---

## 2. Nomes de arquivo

### 2.1 Regra
- Tudo em **minúsculas**, `snake_case`, sem acento.
- ID completo em minúsculas + versão quando o arquivo for entregável final.
- Separador de campo: `__` (duplo underscore).
- Separador interno: `_`.

```
<asset_id_lower>__<state>__v<major>.<minor>.<patch>.<ext>
<asset_id_lower>__<state>__f<frame:04d>.<ext>
```

Exemplos:
```
db_char_hero_goku_base__idle__v1.0.0.png
db_char_hero_goku_base__run__f0012.png
db_equip_weapon_sword_trunks__icon__v1.0.0.png
db_env_namek_sky_day__layer__v1.0.0.png
```

### 2.2 Pastas
Pastas em minúsculas, sem espaços: `characters/canonical_heroes/goku/base/`.

### 2.3 Proibido
- `final.png`, `novo.png`, `teste2.png`, `GokuFinal_v3_OK.png`.
- Espaços, acentos, `#`, `@`, parênteses.
- Renomear asset aprovado sem entrada no `rename_log.json`.

---

## 3. Estrutura de um asset de personagem

```
characters/canonical_heroes/goku/base/
  parts/
    head.png · face_neutral.png · hair_front.png · hair_back.png
    torso.png · pelvis.png · shoulders.png
    upper_arm_f.png · upper_arm_b.png · forearm_f.png · forearm_b.png
    hand_f.png · hand_b.png
    thigh_f.png · thigh_b.png · shin_f.png · shin_b.png
    foot_f.png · foot_b.png
  masks/
    skin.png · hair.png · eyes.png · cloth_primary.png · cloth_secondary.png
  rig/
    rig.json · skeleton.json
  animations/
    idle.json · walk.json · run.json · attack_light_1.json ...
  previews/
    idle.gif · run.gif ...
  db_char_hero_goku_base.json     ← metadata mestre
  icon_128.png
  portrait_256.png
```

---

## 4. Metadados

### 4.1 Registro de asset (obrigatório)
```json
{
  "asset_id": "DB_CHAR_HERO_GOKU_BASE",
  "name": "Goku (Base)",
  "category": "character",
  "subcategory": "hero",
  "version": "1.0.0",
  "status": "APPROVED",
  "session": "S06",
  "created_at": "2026-10-22T00:00:00Z",
  "continuity": "dbz",
  "form": "base",
  "rig": "DB_RIG_HUMANOID_MALE_A",
  "height_px": 220,
  "canvas": [512, 512],
  "ground_y": 448,
  "palette_ref": "palette_master.json#goku",
  "files": [
    {"path": "parts/head.png", "type": "part", "pivot": [256, 264], "layer": 110},
    {"path": "animations/idle.json", "type": "timeline"}
  ],
  "animations": ["idle", "walk", "run", "attack_light_1"],
  "sockets": ["hand_f", "chest", "mouth"],
  "hurtbox": {"type": "ellipse", "size": [44, 190]},
  "masks": ["skin", "hair", "eyes", "cloth_primary"],
  "tags": ["saiyan", "hero", "orange_gi"],
  "license_note": "Fan-derived, non-commercial without authorization",
  "checksums": {"parts/head.png": "sha256:..."}
}
```

### 4.2 Campos por tipo

| Tipo | Campos adicionais |
|---|---|
| `character` | `rig`, `height_px`, `parts[]`, `animations[]`, `masks[]`, `sockets[]`, `hurtbox`, `portrait` |
| `equipment` | `slot`, `covers[]`, `layer`, `pivot`, `compatible_rigs[]`, `grip_pose`, `two_handed` |
| `skill` | `element`, `components[]`, `cast_time`, `cooldown`, `hit_frames[]`, `screen_coverage` |
| `vfx` | `element`, `blend`, `anchor`, `fps`, `loop`, `frames`, `screen_coverage` |
| `environment` | `layer`, `parallax`, `tileable`, `size_px`, `palette` |
| `map` | `viewport`, `world_width`, `ground_band`, `colliders`, `spawns`, `portals`, `occluders` |
| `ui` | `nine_slice`, `states[]`, `text_free`, `theme_ref` |
| `icon` | `source_asset`, `safe_area`, `sizes[]`, `rarity` |

### 4.3 Valores de `status`
`PLANNED` · `GENERATED` · `PROCESSING` · `QA_PENDING` · `APPROVED` · `REWORK_REQUIRED` · `BLOCKED` · `DEPRECATED`

---

## 5. Manifesto

`asset_manifest.json` na raiz do pack:

```json
{
  "pack": "dragonball-aqw-asset-pack",
  "version": "0.1.0",
  "matrix_version": "0.0.0",
  "generated_at": "2026-10-22T00:00:00Z",
  "assets": [],
  "atlases": [],
  "stats": {"characters": 0, "equipment": 0, "enemies": 0, "vfx": 0, "maps": 0, "ui": 0}
}
```

- Começa vazio (nenhum asset aprovado ainda).
- É reconstruído por `tools/build_manifest.py` a partir dos metadados — nunca editado à mão depois do G4.

---

## 6. Versionamento

| Mudança | Bump |
|---|---|
| Correção de arte sem mudar pivô/nome | `PATCH` |
| Novo clipe, nova peça, novo estado | `MINOR` |
| Mudança de pivô, altura, rig, ordem de camada | `MAJOR` |
| Renomear ID | `MAJOR` + `rename_log.json` |

- `matrix_version` é global e só muda no congelamento.
- Assets declaram a `matrix_version` de origem.
- Compatibilidade: consumidor deve aceitar campos extras; produtor não remove campos obrigatórios sem `MAJOR`.

---

## 7. `rename_log.json`

```json
[
  {
    "from": "DB_CHAR_HERO_GOKU_IDLE",
    "to": "DB_CHAR_HERO_GOKU_BASE_IDLE",
    "reason": "separar forma base de transformações",
    "version": "2.0.0",
    "date": "2026-10-22"
  }
]
```

Nenhum ID aprovado é renomeado sem entrada aqui.

---

## 8. Convenções JSON

- UTF-8 sem BOM, LF, indentação 2 espaços, newline final.
- Chaves em `snake_case`, inglês.
- Números: px inteiros; ângulos e escalas em float com até 4 casas.
- `null` explícito em vez de campo ausente quando o schema exigir.
- Ordenação alfabética em arquivos gerados.
- Sem comentários (JSON estrito).
- Todo arquivo valida contra um schema em `standards/`.

---

## 9. Checklist de naming/metadados

- [ ] ID único e no regex.
- [ ] Categoria/subcategoria da lista.
- [ ] Arquivo em lowercase snake.
- [ ] Versão presente no entregável final.
- [ ] Metadados com todos os campos obrigatórios do tipo.
- [ ] Checksums gerados.
- [ ] `rig_compat` existente.
- [ ] `layer` presente em `layer_order.json`.
- [ ] `matrix_version` declarada.
- [ ] Renomeações registradas.
