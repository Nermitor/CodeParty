from data import db_session
db_session.global_init("db/db.db")

from app_settings import app
from core.recomendations.index import index
from apps import authorisation, profile, posts

import views  # do not delete, connects views on import
from data.models import languages

langs = [['1C', '1c'], ['ARM assembler', 'armasm'], ['Bash', 'bash'], ['C#', 'csharp'], ['C', 'c'], ['C++', 'cpp'],
         ['CSS', 'css'], ['Dart', 'dart'], ['Delphi', 'dpr'], ['Erlang', 'erlang'], ['F#', 'fsharp'],
         ['Fortran', 'fortran'], ['Go', 'go'], ['GraphQL', 'graphql'], ['HTML, XML', 'xml'], ['Haskell', 'haskell'],
         ['JSON', 'json'], ['Java', 'java'], ['JavaScript', 'javascript'], ['Kotlin', 'kotlin'], ['Lisp', 'lisp'],
         ['Lua', 'lua'], ['Markdown', 'markdown'], ['PHP', 'php'], ['Perl', 'perl'], ['Plaintext', 'plaintext'],
         ['PowerShell', 'powershell'], ['Prolog', 'prolog'], ['Python', 'python'], ['Python REPL', 'python-repl'],
         ['Ruby', 'ruby'], ['Rust', 'rust'], ['SQL', 'sql'], ['Scala', 'scala'], ['Shell', 'shell'], ['Swift', 'swift'],
         ['TypeScript', 'typescript'], ['x86 Assembly', 'x86asm'], ['YAML', 'yml']]






if __name__ == '__main__':

    index()
    app.register_blueprint(authorisation.app.authorisation)
    app.register_blueprint(profile.app.profile)
    app.register_blueprint(posts.app.posts)
    app.run()
