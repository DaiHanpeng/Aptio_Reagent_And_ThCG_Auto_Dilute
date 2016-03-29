# -*- mode: python -*-
a = Analysis(['D:\\01_Automation\\23_Experiential_Conclusions_2016\\03_Reagent_And_ThCG_Auto_Dilute\\Python\\TimingScanner.py'],
             pathex=['D:\\01_Automation\\23_Experiential_Conclusions_2016\\03_Reagent_And_ThCG_Auto_Dilute\\Python'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='TimingScanner.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
