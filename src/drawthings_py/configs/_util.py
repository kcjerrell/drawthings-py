from drawthings_py.configs.config_dict import ConfigDict
from drawthings_py.configs.gen_config import GenConfig
from drawthings_py.configs.enums import sampler_type_from_value


def describe_config(config: GenConfig | ConfigDict) -> str:
    cd = config._d if isinstance(config, GenConfig) else config  # pyright: ignore[reportPrivateUsage]

    #  flux_klein.cktp, 1024x1024, Strength: 0.9, 20 steps.
    # EulerA sampler, CFG: 2.5, Shift: auto, flux_turbo.ckpt and
    # flux_boobs.skpt lora

    leading: list[str] = []
    if model := cd.get("model"):
        leading.append(model)
    if (width := cd.get("width")) and (height := cd.get("height")):
        leading.append(f"{width}x{height}")

    # Strength (omit when 1.0) and steps
    mid: list[str] = []
    if (strength := cd.get("strength")) is not None and float(strength) != 1.0:
        mid.append(f"Strength: {strength}")
    if steps := cd.get("steps"):
        mid.append(f"{steps} steps")

    # Sampler, CFG (guidance), shift, and loras
    tail: list[str] = []
    if (sampler := cd.get("sampler")) is not None:
        tail.append(f"{sampler_type_from_value(sampler)} sampler")
    if (guidance := cd.get("guidance")) is not None:
        tail.append(f"CFG: {guidance}")

    # Shift: "auto" when resolution_dependent_shift is True
    if cd.get("resolution_dependent_shift"):
        shift_val: str | float | None = "auto"
    else:
        shift_val = cd.get("shift")
    if shift_val is not None:
        tail.append(f"Shift: {shift_val}")

    # Loras: list filenames
    lora_files: list[str] = []
    if loras := cd.get("loras"):
        for lora in loras:
            f = lora.get("file")
            if f:
                lora_files.append(f)
    if lora_files:
        if len(lora_files) == 1:
            lf = lora_files[0]
        elif len(lora_files) == 2:
            lf = f"{lora_files[0]} and {lora_files[1]}"
        else:
            lf = ", ".join(lora_files[:-1]) + f", and {lora_files[-1]}"
        tail.append(f"{lf} lora")

    # Build the final description
    parts: list[str] = []
    if leading:
        first = ", ".join(leading)
        if mid:
            first = f"{first}, {', '.join(mid)}."
        else:
            first = f"{first}."
        parts.append(first)

    if tail:
        parts.append(", ".join(tail))

    return " ".join(parts).strip()
