# Copyright 2021-2024 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from functools import lru_cache
from typing import Type

from .._manager._manager_factory import _ManagerFactory
from ..common import _utils
from ..common._check_dependencies import _TAIPY_ENTERPRISE_CORE_MODULE, _using_enterprise
from ._version_fs_repository import _VersionFSRepository
from ._version_manager import _VersionManager


class _VersionManagerFactory(_ManagerFactory):
    __REPOSITORY_MAP = {"default": _VersionFSRepository}

    @classmethod
    @lru_cache
    def _build_manager(cls) -> Type[_VersionManager]:
        if _using_enterprise():
            version_manager = _utils._load_fct(
                _TAIPY_ENTERPRISE_CORE_MODULE + "._version._version_manager", "_VersionManager"
            )  # type: ignore
            build_repository = _utils._load_fct(
                _TAIPY_ENTERPRISE_CORE_MODULE + "._version._version_manager_factory", "_VersionManagerFactory"
            )._build_repository  # type: ignore
        else:
            version_manager = _VersionManager
            build_repository = cls._build_repository
        version_manager._repository = build_repository()  # type: ignore
        return version_manager  # type: ignore

    @classmethod
    @lru_cache
    def _build_repository(cls):
        return cls._get_repository_with_repo_map(cls.__REPOSITORY_MAP)()
