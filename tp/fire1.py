import fire


def hello(name="World"):
    """
    一个简单的函数，打印问候语。
    :param name: 接收一个名字作为参数，默认为 World。
    """
    print(f"Hello, {name}!")


if __name__ == "__main__":
    fire.Fire(hello)