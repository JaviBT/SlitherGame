
import cx_Freeze

executables = [cx_Freeze.Executable("slither.py")]

cx_Freeze.setup(
    name="Slither",
    options={"build_exe":{"packages":{"pygame","os","sys","random"},"include_files":{"assets"}}},
    description="The Slither game made by JaviBT",
    executables = executables
)
