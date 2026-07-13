#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/motorola/vienna',
    'hardware/google/interfaces',
    'hardware/google/pixel',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/motorola',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    # Avoid pulling sensors-V2 alongside sensorservice-V1 (sensors-V3).
    'android.hardware.sensors-V2-ndk': lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/lib64/hw/hwcomposer.mtk_common.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    'vendor/lib64/hw/mt6878/vendor.mediatek.hardware.pq_aidl-impl.so': blob_fixup()
        .add_needed('libui_shim.so'),
    (
        'vendor/bin/hw/mt6878/android.hardware.graphics.allocator-V2-service-mediatek.mt6878',
        'vendor/lib64/egl/mt6878/libGLES_mali.so',
        'vendor/lib64/hw/mt6878/android.hardware.graphics.allocator-V2-mediatek.so',
        'vendor/lib64/hw/mt6878/android.hardware.graphics.mapper@4.0-impl-mediatek.so',
        'vendor/lib64/hw/mt6878/mapper.mediatek.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V2-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V4-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V7-ndk.so',
    ): blob_fixup()
        .replace_needed(
            'android.hardware.graphics.common-V4-ndk.so',
            'android.hardware.graphics.common-V7-ndk.so',
        ),
    'vendor/lib64/mt6878/libpqconfig.so': blob_fixup()
        .replace_needed(
            'android.hardware.sensors-V2-ndk.so',
            'android.hardware.sensors-V3-ndk.so',
        ),
    'vendor/lib64/librt_extamp_intf.so': blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v31.so'),
    (
        'vendor/lib64/libnvram.so',
        'vendor/lib64/libsysenv.so',
    ): blob_fixup()
        .add_needed('libbase_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'vienna',
    'motorola',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
