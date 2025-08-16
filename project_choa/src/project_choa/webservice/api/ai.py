import tracemalloc
from dotenv import load_dotenv

from openai import AsyncOpenAI
from api.core_and_router import Router
from api.accounting import Accounting
from api.ask import Ask
from api.analyze import Analyze
from api.joke import Joke
tracemalloc.start()


# создаем класс ChoaAI
class ChoaAI():

    load_dotenv()

    def __init__(self):
        self.client = AsyncOpenAI()
        self.user_context = {}

    # метод вызова нейро-финансиста
    async def neuro_finansist(self, user_id: int, note: str):
        if user_id not in self.user_context:
            self.user_context[user_id] = ''

        router = Router(note, self.user_context[user_id], self.client)
        output = await router.activate()
        self.user_context[user_id] += note

        if 'accounting' in output:
            accounting = Accounting(note, self.user_context[user_id], self.client)
            out_answer, was_written = await accounting.activate()

            if was_written == True:
                self.user_context[user_id] = ''
                return 'Спасибо, внесла операцию в журнал'
            else:
                ask = Ask(out_answer, self.client)
                questions = await ask.activate()
                self.user_context[user_id] += questions
                return questions
            
        elif 'analyze' in output:
            analyze = Analyze(self.client)
            out_answer = await analyze.activate()
            return out_answer
        
        elif 'error' in output:
            joke = Joke(note, self.client)
            out_answer = await joke.activate()
            return out_answer
        else:
            return 'Error router'