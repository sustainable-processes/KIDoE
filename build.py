import os
import shutil
from pathlib import Path

import PyInstaller.__main__

package_dir = Path(__file__).parent.absolute()
path_to_main = f'{package_dir}/cli.py'

def install():
    PyInstaller.__main__.run([
        path_to_main,
        '--name', 'kidoe',
        '--onedir',
        '--clean',
        '--noconfirm',
        '--copy-metadata', 'moocore',
        '--collect-all', 'pymoo',
        '--add-data', f'{package_dir}/ontology:kidoe/ontology',
    ])

    conda_prefix = os.environ.get('CONDA_PREFIX')
    if not conda_prefix:
        raise RuntimeError('No active conda environment found (CONDA_PREFIX not set)')
    env_prefix = Path(conda_prefix)

    install_dir = env_prefix / 'lib' / 'kidoe'
    if install_dir.exists():
        shutil.rmtree(install_dir)
    shutil.copytree('dist/kidoe', install_dir)

    symlink = env_prefix / 'bin' / 'kidoe'
    print(symlink)
    if symlink.exists() or symlink.is_symlink():
        symlink.unlink()
    symlink.symlink_to(install_dir / 'kidoe')

    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('build', ignore_errors=True)
    Path('kidoe.spec').unlink(missing_ok=True)