 """
    # Contestants
    bob_npc = NPC("Bob", PersonalityType.BoardGameEnthusiast)
    #player = Player("Jacob", "Auckland, NZ", "Digital Analytics Intern")

    contestants_queue = Queue()
    #contestants_queue.put(player)
    contestants_queue.put(bob_npc)

    num_questions_to_ask = 3
    for i in range(num_questions_to_ask):
        print(f'= ROUND {i+1} =')
        current_contestant = contestants_queue.get()
        contestants_queue.put(current_contestant)

        print(current_contestant.name)

        trivia_question = TriviaQuestion(TriviaQuestionDifficulties.EASY, QuestionTypes.MULTIPLE, TriviaQuestionCategory.Sports)

        print('\nQ: ', trivia_question.question)
        for i, choice in enumerate(trivia_question._choices):
            print(f'{i+1}) {choice}')

        response = current_contestant.get_response(PromptTypes.TRIVIA_QUESTION, prompt=trivia_question)

        if isinstance(current_contestant, NPC):
            print(f'\n{current_contestant.name} : {response}')

        if trivia_question.check_answer(response):
            print("Correct!")
        else:
            print("Wrong!")
        
        print()
        """