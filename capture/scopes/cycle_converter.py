# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0


def convert_num_cycles(cfg: dict, scope_type: str) -> int:
    """ Converts number of cycles to number of samples if samples not given.

    As the scopes are configured in number of samples, this function converts
    the number of cycles to samples.
    The number of samples must be divisble by 3 for batch captures on Husky
    and is adjusted accordingly.

    Args:
        dict: The scope configuration.
        scope_type: The used scope (Husky or WaveRunner).

    Returns:
        The number of samples.
    """
    if cfg[scope_type].get("num_samples") is None:
        sampl_target_rat = cfg[scope_type].get("sampling_rate") / cfg["target"].get("target_freq")
        num_samples = int(cfg[scope_type].get("num_cycles") * sampl_target_rat)

        if scope_type == "husky":
            if num_samples % 3:
                num_samples = num_samples + 3 - (num_samples % 3)

        return num_samples
    else:
        return cfg[scope_type].get("num_samples")


def convert_offset_cycles(cfg: dict, scope_type: str) -> int:
    """ Converts offset in cycles to offset in samples if not given in samples.

    Args:
        dict: The scope configuration.
        scope_type: The used scope (Husky or WaveRunner).

    Returns:
        The offset in samples.
    """
    if cfg[scope_type].get("offset_samples") is None:
        sampl_target_rat = cfg[scope_type].get("sampling_rate") / cfg["target"].get("target_freq")
        return int(cfg[scope_type].get("offset_cycles") * sampl_target_rat)
    else:
        return cfg[scope_type].get("offset_samples")
