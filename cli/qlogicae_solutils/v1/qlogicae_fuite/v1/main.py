
def main():
    from importlib.metadata import version

    print(
        version("qlogicae-fuite")
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
