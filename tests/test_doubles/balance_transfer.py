from sturdy import resolve, ICommand, CommandException


class PluginLoadCommand(ICommand):
    def __call__(self) -> None:
        resolve(
            "IoC.Register",
            "BalanceTransfer.CreateAccount",
            lambda *args: Account(*args),
        )()
        resolve(
            "IoC.Register",
            "BalanceTransfer.CreateTransferInfo",
            lambda *args: TransferInfo(*args),
        )()
        resolve(
            "IoC.Register",
            "BalanceTransfer.CheckSenderBalanceCommand",
            lambda *args: CheckSenderBalanceCommand(*args),
        )()
        resolve(
            "IoC.Register",
            "BalanceTransfer.CheckReceiverBalanceCommand",
            lambda *args: CheckReceiverBalanceCommand(*args),
        )()
        resolve(
            "IoC.Register",
            "BalanceTransfer.ChangeBalanceCommand",
            lambda *args: ChangeBalanceCommand(*args),
        )()
        resolve(
            "IoC.Register",
            "BalanceTransfer.PerformBalanceTransferCommand",
            lambda *args: PerformBalanceTransferCommand(*args),
        )()


class Account:
    def __init__(
        self, current_balance: int, min_balance: int = 0, max_balance: int = 1000
    ) -> None:
        self.current_balance = current_balance
        self.min_balance = min_balance
        self.max_balance = max_balance


class TransferInfo:
    def __init__(self, sender: Account, receiver: Account, value: int) -> None:
        self.sender = sender
        self.receiver = receiver
        self.value = value

    def __str__(self) -> str:
        return f"sender: {self.sender}; receiver: {self.receiver}, value: {self.value}"


class ChangeBalanceCommand(ICommand):
    def __init__(self, account: Account, value: int) -> None:
        self.__account = account
        self.__value = value

    def __call__(self) -> None:
        self.__account.current_balance += self.__value


class CheckSenderBalanceCommand(ICommand):
    def __init__(self, transfer: TransferInfo) -> None:
        self.__transfer = transfer

    def __call__(self) -> None:
        sender = self.__transfer.sender
        sender_current_balance = sender.current_balance
        sender_min_balance = sender.min_balance

        value = self.__transfer.value

        new_balance = sender_current_balance - value
        if new_balance < sender_min_balance:
            raise CommandException


class CheckReceiverBalanceCommand(ICommand):
    def __init__(self, transfer: TransferInfo) -> None:
        self.__transfer = transfer

    def __call__(self) -> None:
        receiver = self.__transfer.receiver
        receiver_current_balance = receiver.current_balance
        receiver_max_balance = receiver.max_balance

        value = self.__transfer.value

        new_balance = receiver_current_balance + value
        if new_balance > receiver_max_balance:
            raise CommandException


class PerformBalanceTransferCommand(ICommand):
    def __init__(self, transfer: TransferInfo) -> None:
        self.__transfer = transfer

    def __call__(self) -> None:
        c1 = resolve("BalanceTransfer.CheckSenderBalanceCommand", self.__transfer)
        c2_do = resolve(
            "BalanceTransfer.ChangeBalanceCommand",
            self.__transfer.sender,
            -self.__transfer.value,
        )
        c2_undo = resolve(
            "BalanceTransfer.ChangeBalanceCommand",
            self.__transfer.sender,
            self.__transfer.value,
        )
        c3 = resolve("BalanceTransfer.CheckReceiverBalanceCommand", self.__transfer)
        c4_do = resolve(
            "BalanceTransfer.ChangeBalanceCommand",
            self.__transfer.receiver,
            self.__transfer.value,
        )
        c4_undo = resolve(
            "BalanceTransfer.ChangeBalanceCommand",
            self.__transfer.receiver,
            -self.__transfer.value,
        )

        transaction = resolve(
            "SimpleTransaction.CreateTransaction",
            [c1, (c2_do, c2_undo), c3, (c4_do, c4_undo)],
        )

        transaction()
