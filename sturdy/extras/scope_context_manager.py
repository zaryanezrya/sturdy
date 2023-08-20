from sturdy import resolve, ICommand


class RunInScope:
    def __init__(self, scope) -> None:
        self.scope = scope
        self.prev_scope = resolve("Scopes.Current")

    def __enter__(self):
        resolve("Scopes.Current.Set", self.scope)()

    def __exit__(self, type, value, traceback):
        resolve("Scopes.Current.Set", self.prev_scope)()


class RunInNewScope:
    def __init__(self) -> None:
        self.prev_scope = resolve("Scopes.Current")
        self.scope = resolve("Scopes.New", self.prev_scope)

    def __enter__(self):
        resolve("Scopes.Current.Set", self.scope)()

    def __exit__(self, type, value, traceback):
        resolve("Scopes.Current.Set", self.prev_scope)()


class LoadPluginCommand(ICommand):
    def __call__(self) -> None:
        resolve("IoC.Register", "Scopes.RunInScope", lambda scope: RunInScope(scope))()
        resolve("IoC.Register", "Scopes.RunInNewScope", lambda: RunInNewScope())()
