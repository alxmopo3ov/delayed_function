ya_make_template = """PROGRAM({program_name})

OWNER({owner})

PY_SRCS(
    __main__.py
)

PEERDIR(
    {auto_ml_root}
    {library_root}
)

END()
"""