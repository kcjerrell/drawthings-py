from drawthings_py.types import Config

klein4 = Config(
    {
        "model": "flux_2_klein_4b_q6p.ckpt",
        "width": 1024,
        "height": 768,
        "seed": -1,
        "strength": 1,
        "steps": 4,
        "guidance_scale": 1,
        "sampler": 16,
        "stochastic_sampling_gamma": 0.3,
        "shift": 3,
    }
)

chroma = Config(
    {
        "cfg_zero_star": True,
        "guidance_scale": 2.5,
        "steps": 8,
        "loras": [
            {
                "mode": "all",
                "file": "hyper_flux.1__dev__8_step_lora_f16.ckpt",
                "weight": 0.6,
            },
            {"mode": "all", "file": "flux_1_depth_dev_lora_f16.ckpt", "weight": 1},
            {
                "mode": "all",
                "file": "flux.1__dev__to__schnell__4_step_lora_f16.ckpt",
                "weight": 0.34,
            },
        ],
        "seed": -1,
        "height": 512,
        "sampler": 17,
        "width": 1024,
        "resolution_dependent_shift": True,
        "speed_up_with_guidance_embed": True,
        "model": "chroma_1_hd_q5p.ckpt",
        "strength": 1,
        # "shift": 3.1581929,
    }
)

chroma_dep = Config(
    {
        "cfg_zero_star": True,
        "guidance_scale": 2.5,
        "steps": 8,
        "loras": [
            {
                "mode": "all",
                "file": "hyper_flux.1__dev__8_step_lora_f16.ckpt",
                "weight": 0.6,
            },
            {"mode": "all", "file": "flux_1_depth_dev_lora_f16.ckpt", "weight": 1},
            {
                "mode": "all",
                "file": "flux.1__dev__to__schnell__4_step_lora_f16.ckpt",
                "weight": 0.34,
            },
        ],
        "seed": -1,
        "height": 512,
        "sampler": 17,
        "width": 1024,
        "resolution_dependent_shift": True,
        "speed_up_with_guidance_embed": True,
        "model": "chroma_1_hd_q5p.ckpt",
        "strength": 1,
        "shift": 3.1581929,
    }
)

flux_canny = Config(
    {
        "guidance_scale": 4.5,
        "controls": [
            {
                "weight": 1,
                "global_average_pooling": False,
                "input_override": "softedge",
                "file": "controlnet_union_pro_flux_1_dev_2.0_q8p.ckpt",
                "no_prompt": False,
                "guidance_start": 0,
                "guidance_end": 1,
                "target_blocks": [],
                "control_importance": "balanced",
                "down_sampling_rate": 1,
            }
        ],
        "model": "980131_atomixfluxunet_v10_q8p.ckpt",
        "resolution_dependent_shift": True,
        "steps": 28,
        "seed": -1,
        "seed_mode": 2,
        "sampler": 10,
        "shift": 2.6555896,
        "height": 512,
        "speed_up_with_guidance_embed": True,
        "strength": 1,
        "width": 768,
    }
)
