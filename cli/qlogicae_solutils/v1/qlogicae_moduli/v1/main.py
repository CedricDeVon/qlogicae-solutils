
def main():
    from importlib.metadata import version

    print(
        version("qlogicae-moduli")
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
