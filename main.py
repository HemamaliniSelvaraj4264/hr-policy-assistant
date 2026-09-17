from hr_assistant.pipeline import ask,build_hr_assistant

def main():
    print("Building the HR Policy assistant...")
    agent = build_hr_assistant()
    print("Assistant Ready..")

    demo_question = [
        "How many paid annual leave days do I get?",
        "What is the notice period during probation?",
        "Can I work from home every day?"
    ]

    for question in demo_question:
        print("=" * 40)
        print("Question:", question)
        print("-" * 40)
        answer = ask(agent,question)
        print("Answer:", answer)
        print("=" * 40)
        print()


if __name__ == "__main__":
    main()
