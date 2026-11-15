
def main():
    from library.application_manager import ApplicationManager

    result = (
        ApplicationManager()
            .get_singleton()
            .run()
    )

    return result


if __name__ == "__main__":
    raise SystemExit(main())

