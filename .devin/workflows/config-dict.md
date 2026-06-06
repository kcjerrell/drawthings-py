# ConfigDict and FlatBuffer Consistency Workflow

You are working in the `dt-grpc-py` repository.

## Goal

Review and update the configuration typing and FlatBuffer build path so the public Python config API is consistent with `resources/config.fbs`, while using the public field/type names described below.

Primary files:

- `src/drawthings_py/configs/types.py`
- `resources/config.fbs`
- `src/drawthings_py/configs/_gen_config.py`

## Type Consistency Review

Compare `src/drawthings_py/configs/types.py` against `resources/config.fbs`.

Ensure all FlatBuffer enums and tables that are part of configuration input are represented correctly as Python `IntEnum`s and `TypedDict`s:

- Enum members must match the `.fbs` definitions in name and integer value.
- TypedDict fields must match the `.fbs` schema semantically, with the public Python names listed below.
- TypedDict value types should match the FlatBuffer field types as closely as practical for the public API.
- Enum-valued fields should accept the corresponding enum, integer values, and string enum names where that is the existing/public pattern.
- Nested vectors should be typed as Python lists.

Rename these TypedDict classes:

- `Control` -> `ControlDict`
- `LoRA` / `Lora` -> `LoraDict`
- FlatBuffer `GenerationConfiguration` input -> `ConfigDict`

Keep exports/imports consistent after the rename, including `src/drawthings_py/configs/__init__.py` and any references in tests or package modules.

## ConfigDict Field Names

`ConfigDict` is the public API and should not blindly mirror every FlatBuffer field name. Apply these public field renames:

- `start_width` -> `width`
- `start_height` -> `height`
- `guidance_scale` -> `guidance`
- `motion_bucket_id` -> `motion_scale`
- `cond_aug` -> `guiding_frame_noise`
- `start_frame_cfg` -> `start_frame_guidance`

Also preserve the existing public hires-fix names:

- `hires_fix_start_width` should be represented as `hires_fix_width`
- `hires_fix_start_height` should be represented as `hires_fix_height`

Exclude these FlatBuffer fields from `ConfigDict`:

- `id`
- `batch_count`
- `image_guidance_scale`
- `decode_with_attention`
- `hires_fix_decode_with_attention`
- `clip_weight`
- `image_prior_steps`
- `stage_2_steps`
- `stage_2_cfg`
- `stage_2_shift`

Do not add excluded fields back through aliases.

Check whether `ConfigDict` is missing any non-excluded fields from `GenerationConfiguration` in `resources/config.fbs`. Add any missing fields with appropriate public names and types. In particular, verify fields such as `fps_id` and `causal_inference_enabled` are represented if they are part of the schema and not excluded.

## build_config()

After the type review, review and implement or verify `src/drawthings_py/configs/_gen_config.py`.

`build_config()` should:

- Take a `ConfigDict`.
- Return FlatBuffer bytes for a `GenerationConfiguration`.
- Include every field supplied by the input config, mapped to the correct FlatBuffer field.
- Preserve the optional `seed` parameter behavior if present: when `seed` is not `None`, it should override `config["seed"]` in the built FlatBuffer.
- Correctly build nested `controls` and `loras` vectors.
- Correctly build FlatBuffer strings before table construction.
- Convert enum values accepted by `ConfigDict` into the generated FlatBuffer enum integer values.

Public-to-FlatBuffer field mapping must include:

- `width` -> `start_width`
- `height` -> `start_height`
- `guidance` -> `guidance_scale`
- `motion_scale` -> `motion_bucket_id`
- `guiding_frame_noise` -> `cond_aug`
- `start_frame_guidance` -> `start_frame_cfg`
- `hires_fix_width` -> `hires_fix_start_width`
- `hires_fix_height` -> `hires_fix_start_height`

Before adding numeric size fields to `GenerationConfiguration`, divide the input value by `64` and round to the nearest `int` for:

- `crop_top`
- `crop_left`
- Any `ConfigDict` field with `width` in its name.
- Any `ConfigDict` field with `height` in its name.
- Any `ConfigDict` field with `overlap` in its name.

The conversion applies to the value written to the FlatBuffer, not to the caller's input dictionary.

Change the effective default from the `.fbs` default for:

- `seed_mode`: default to `SeedMode.ScaleAlike` when the caller does not provide `seed_mode`.

Do not emit excluded `ConfigDict` fields in the builder. The FlatBuffer may still use schema defaults for fields that are absent from the public input.

## Testing Expectations

Add or update focused tests where useful. At minimum, verify:

- The renamed TypedDicts and public exports import successfully.
- Old removed public fields such as `guidance_scale` are no longer used by tests.
- `build_config()` returns bytes that parse as `GenerationConfiguration`.
- Public renamed fields are written to the matching FlatBuffer accessors.
- Width/height/overlap/crop fields are divided by `64` and rounded before storage.
- `seed` argument overrides config seed.
- `seed_mode` defaults to `SeedMode.ScaleAlike`.
- Nested `controls` and `loras` round-trip through the generated FlatBuffer accessors.

## Verification

Unless instructed otherwise, verify with:

```bash
poetry run mypy
poetry run ruff check
poetry run basedpyright
poetry run pytest
```

If any command fails, fix the issue or document the remaining blocker with the exact failing command and reason.
