from cx_Freeze import setup, Executable

#target = Executable(
#    script='main.py',
#    icon='icon.ico'
#)

executables = [
    Executable(script='main.py',
               icon='icon.ico',
               base='Win32GUI')
]

setup(
    name="Ensayos_UCS",
    version=1.05,
    description="Software enfocado en determinar parametros pre-peak",
    executables=executables,
    author='Sergio Flores'
    #icon='icon.ico'
    #packages=['scipy.optimize', 'scipy.integrate']

)