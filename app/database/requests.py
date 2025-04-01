from app.database.models import async_session
from app.database.models import User_info, User_sub, User_messages,User_log
from sqlalchemy import select, update, func

from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from app.outputEndSub import get_remaining_time
import tiktoken

text_from_file = """Базовые потребности = Базовые убеждения.
ПОТРЕБНОСТЬ В ФИЗИЧЕСКОЙ БЕЗОПАСНОСТИ.
Удовлетворение потребности в праве на жизнь, физическую целостность/безопасность, свободу, еду, воду, тепло, жилье.

Здоровые (взрослые) базовые убеждения – мое здоровье, жизнь важны, я имею право быть здоровым, я имею право жить, быть свободным, быть в физической безопасности, заботиться о своем здоровье, выделять на это силы, время, деньги и пр.

Поврежденные убеждения, сформированные вследствие травматизации – я не обращаю внимание на свое здоровье, не лечусь, не ухаживаю за внешностью, играю со смертью (занимаюсь чем-то экстремальным, с риском для жизни и здоровья), самоповреждаю себя, имею суицидальные мысли и попытки. 
Я не имею права быть, моя жизнь не важна, мне угрожает опасность, меня можно бить …

ПОТРЕБНОСТЬ В ЛЮБВИ И ПРИНЯТИИ.
Удовлетворение потребности происходит через заботу и принятие человека таким, какой он есть с его внешностью, полом, физическими, эмоциональными и интеллектуальными способностями и особенностями. Потребность быть важным и ценным для «своих».

Здоровые (взрослые) базовые убеждения – я ценный, важный, достойный человек. Я имею право, чтобы обо мне заботились, любили таким, какой я есть. Я имею право быть собой. Я хороший человек. Я имею право привлекать внимание к себе. Я достоин того, чтобы со мной общались, давали мне внимание, заботились и принимали. Я такой же ценный человек, как и другие. Я имею право быть счастливым, я имею право на достойную жизнь и хорошие отношения.

Поврежденные убеждения, сформированные вследствие травматизации – если я не соответствую ожиданиям других, то я не ценный. Такой, какой я есть я не ценный, недостойный, другие важнее меня. Я плохой, я дефективный (глупый, некрасивый, эмоционально нестабильный..)   Я виноват в том, что ко мне плохо относятся, я виноват, если кто-то недоволен моим присутствием. Другие важнее чем я. Я не имею права на принятие и уважение. Я не достоин заботы и любви. Другие люди могут вести себя со мной, как им вздумается, они более важные, а я не имею права им противоречить.

ПОТРЕБНОСТЬ В СОЦИАЛЬНЫХ ОТНОШЕНИЯХ И ПОМОЩИ.
Потребность быть с другими, быть как все, чтобы выжить, принадлежать группе, быть частью «своих»

Здоровые (взрослые) базовые убеждения – Я имею право на хорошее отношение к себе. Имею право на помощь. Я имею право чего-то не знать, не уметь и при этом я остаюсь ценным. Я такой же ценный, как другие. Я имею право, чтобы мне уделяли время, чтобы мне объясняли, учили, давали время и создавали условия для моего роста.

Поврежденные убеждения, сформированные вследствие травматизации-чтобы быть в отношениях я должен жертвовать собой и своими интересами, интересы других важнее моих. Я всегда все должен делать сам, не имею права просить о помощи. Я не должен отвлекать других своими проблемами, я должен сам во всем разбираться. Если я чего-то не умею или не знаю, если кто-то недоволен моими знаниями и умениями, то я глупый. Я не имею права отвлекать людей, просить, чтобы мне объяснили, научили, рассказали, ответили на вопросы. Мои интересы не такие важные, как интересы семьи. Я должен довольствоваться лишь необходимым, не просить большего. Я недостоин, не имею права, чтобы на меня и мои интересы тратили деньги.

ПОТРЕБНОСТЬ В АВТОНОМИИ.
 Потребность быть собой, быть уникальным, особенным, отличаться от других, иметь личные границы, т.е. свое мнение, проявлять эмоции, иметь свое пространство, место, время, деньги, желания и нежелания.
ФОРМИРОВАНИЕ ХОЧУ/НЕ ХОЧУ
Здоровые (взрослые) базовые убеждения – мои желания//нежелания важны и ценны, я имею право хотеть или не хотеть. Я имею право иметь свое мнение, оно может отличаться от других, но оно ценное для меня. Я могу отличаться от других, быть уникальным и особенным и при этом быть в безопасности, быть принятым и любимым таким, какой я есть. Я имею право не соответствовать ожиданиям других людей. Для меня важны мои эмоции, и я имею право их чувствовать. Я имею право не делиться тем, чем я хочу, имею право иметь свои тайны. Мое время ценно для меня, я имею право уделять себе время и выделять себе время на другие вещи настолько, насколько  мне это интересно и полезно. Я имею право иметь свои деньги, вещи, мысли, идеи, пространство. Это важно для меня.
Поврежденные убеждения, сформированные вследствие травматизации-мои желания/нежелания (вещи, время, пространство, деньги и пр.) не важны, желания (другое) других важнее моих. Я не имею право на свое мнение (другое). Если мое мнение/внешность/желания отличаются от других, то это небезопасно, оно не ценно. Если мое мнение не нравится другим, то оно не правильное, глупое. Мнения других важнее моего. Я не имею право отстаивать свое мнение, лучше от него отказаться или постоянно менять в угоду другим. Мои желания глупые, только глупые хотят … Моя эмоциональность – это мой дефект, нормальные люди не такие чувствительные как я. Я некрасивая/толстая/рыжая и т.п., поэтому сама виновата, что ко мне так относятся. Я не получаю того, что хочу, потому что я отличаюсь от других. Иметь свое мнение нельзя, надо со всеми соглашаться, отказываться от своего хочу. Я должна делать то, что нужно другим, а не то, что хочу или нужно мне.

ПОТРЕБНОСТЬ В ДИСЦИПЛИНЕ И КОНТРОЛЕ.
Потребность отделиться от других, контролировать свое пространство, быть ответственным и влиять на результаты своей жизни, принимать решения, иметь границы с другими людьми, не нарушать чужие и отстаивать свои.
ФОРМИРУЕТСЯ МОГУ.
Здоровые (взрослые) базовые убеждения – я имею право развиваться и приобретать опыт в своем темпе. Я имею право брать столько времени, сколько нужно на…,я понимаю свои возможности и имею право взять на себя ответственность лишь за то, что могу сделать. Я имею право не делать того, что не смогу сделать и при этом быть в безопасности и быть ценным, я имею право отказаться, я имею право согласиться. Я имею право на то, чтобы мне объяснили мои права и обязанности. Я имею право на достойные условия жизни/работы. Я имею право контролировать свою жизнь/безопасность. Я имею право принимать решения и брать ответственность за их реализацию. Я имею право поменять решение в любой момент, если мое мнение или условия изменились. Я имею право не брать ответственность или отказаться от нее, если мне стало понятным, что я не смогу обеспечить себе или другим безопасность или достойные условия. Я имею право чего-то не предусмотреть, не знать, и не проконтролировать.
Поврежденные убеждения, сформированные вследствие травматизации-если кто-то недоволен моими результатами (количеством попыток), значит я виновата, я глупая, безответственная. Если я не сделала с первого раза идеально, значит я не должна пробовать еще раз, должна отказаться от действия. Если я что-то не проконтролирую, я в опасности, я виновата, что не получилось. Я должна все знать, все предусмотреть и все проконтролировать, иначе я виновата, что что-то пошло не так, как хотелось. Я не должна передавать ответственность другим людям за их поведение, я должна все терпеть и соглашаться на любые их условия. Обстоятельства/человек сильнее меня, я ничего не могу изменить.
ПОТРЕБНОСТЬ В ПРИЗНАНИИ, ТВОРЧЕСТВЕ И САМОВЫРАЖЕНИИ.
Потребность проявляетсяв совершенствовании своих способностей и развитии талантов, профессиональных навыков. Право иметь время на их развитие, тратить на это деньги. Право иметь свои собственные идеи, свое видение, которое может отличаться от привычных, придавать смыслы. Право на самореализацию, следование своей мечте, интересам. Право на признание, ценность и хорошее отношение в среде своих коллег по интересам.
ФОРМИРУЕТСЯ БУДУ.
Здоровые (взрослые) базовые убеждения мое творчество, мои идеи, опыт, навыки, труд, результаты труда важны. Я имею право делать то, что мне интересно. Я имею право не зависеть от мнения других людей. Другие люди могут быть недовольны моим творчеством, но я могу все равно делать то, что мне интересно, если я не нарушаю их границы. Я имею право привлекать внимание к своему творчеству, отличаться от других. Я достоин получать достойную оплату за хорошо сделанную работу. Я имею право быть не идеальной и развиваться так и столько, сколько я желаю и сколько мне интересно. Имею право сама выбирать        какие способности и таланты и когда развивать. Я слышу мнение других, но имею право не зависеть от него. Я имею право на признание моих коллег, сообщества по интересам. Я имею право менять свои интересы, развивать новые, когда посчитаю необходимым.
Поврежденные убеждения, сформированные вследствие травматизации  - то, что я делаю, не важно и никому не нужно. Мои цели не важны, нужно делать то, что ценно для моих коллег. Если то, что я делаю не нравится другим/это критикуют, то я должна отказаться от этого, другим виднее, что хорошо/что плохо – я не могу претендовать на уникальность. Я сама виновата, что других раздражает мое творчество. Я не должна привлекать внимание своим творчеством, все умеют это делать. Я не должна высовываться и смешить людей, сама виновата, что они критикуют. Если я не первая, то я не важна/лузер, только первые достойны признания. Если я не соответствую критериям моды/стиля/трендам/ пр. я не заслуживаю признания. Я не имею право заниматься тем, что мне интересно, должна делать то, что нужно другим. Творчество других более ценно, мое хуже. Мои смыслы не ценны, нужно следовать смыслам и целям, которые в тренде или важны для других."""


async def set_user(tg_id, username, tg_premium):
    async with async_session() as session:
        user = await session.scalar(select(User_info).where(User_info.user_id == tg_id))

        if not user:
            
            session.add(User_info(user_id=tg_id, user_name=username, tg_premium=tg_premium))
            await session.commit()

async def set_nickname(tg_id, nick):
    async with async_session() as session:
        user = await session.scalar(select(User_info).where(User_info.user_id == tg_id))
        print(user.user_id)

        if user:
            
            await session.execute(
                    update(User_info).where(User_info.user_id == tg_id).values(
                        nickname=nick
                    ))
                
            await session.commit()

async def set_age(tg_id, age):
    async with async_session() as session:
        user = await session.scalar(select(User_info).where(User_info.user_id == tg_id))

        if user:
            
            await session.execute(
                    update(User_info).where(User_info.user_id == tg_id).values(
                        user_age= int(age)
                    ))
                
            await session.commit()

async def set_sex(tg_id, sex):
    async with async_session() as session:
        user = await session.scalar(select(User_info).where(User_info.user_id == tg_id))

        if user:
            
            await session.execute(
                    update(User_info).where(User_info.user_id == tg_id).values(
                        user_sex=sex
                    ))
                
            await session.commit()

async def set_bot_description(tg_id, description):
    async with async_session() as session:
        user = await session.scalar(select(User_info).where(User_info.user_id == tg_id))

        if user:
            
            await session.execute(
                    update(User_info).where(User_info.user_id == tg_id).values(
                        bot_description=description
                    ))
                
            await session.commit()

async def set_bot_name(tg_id, name):
    async with async_session() as session:
        user = await session.scalar(select(User_info).where(User_info.user_id == tg_id))

        if user:
            
            await session.execute(
                    update(User_info).where(User_info.user_id == tg_id).values(
                        bot_name=name
                    ))
                
            await session.commit()

async def success_registration(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User_info).where(User_info.user_id == tg_id))

        if user:
            
            await session.execute(
                    update(User_info).where(User_info.user_id == tg_id).values(
                        is_registered=True
                    ))
                
            await session.commit()

async def is_registered(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User_info).where(User_info.user_id == tg_id))

        if user:
            
            return user.is_registered

async def subscribe(tg_id, sub_name, date):
    async with async_session() as session:
        user = await session.scalar(select(User_info).where(User_info.user_id == tg_id))
        user_sub = await session.scalar(select(User_sub).where(User_sub.user_id == tg_id) )            

        if user_sub:
            if user.sub:
                
                await session.execute(
                    update(User_sub).where(User_sub.user_id == tg_id).values(
                        sub=sub_name,
                        time_sub=date,
                        time_end=date + relativedelta(months=1)
                    ))
                
                await session.commit()
            else:
                user.sub = True
                await session.execute(
                    update(User_sub).where(User_sub.user_id == tg_id).values(
                        sub=sub_name,
                        time_sub=date,
                        time_end=date + relativedelta(months=1)
                    ))

                await session.commit()
        else:
            user.sub = True
            session.add(User_sub(user_id=tg_id, sub=sub_name, time_sub=date, time_end=date + relativedelta(months=1)))
            await session.commit()

async def set_user_message(tg_id, username,is_trial, message, answer, time_mes, time_answ):
    async with async_session() as session:
        session.add(User_messages(user_id=tg_id, user_name=username,is_trial=is_trial, message=message,
                                  answer=answer, time_message=time_mes, time_answer=time_answ))
        await session.commit()
        
async def check_amount_messages(tg_id):
    async with async_session() as session:
        user_messages = await session.execute(select(User_messages).where(User_messages.user_id == tg_id))
        stmt = select(
            User_info.user_id,
            func.row_number().over(order_by=User_info.user_id).label("row_num")
        ).subquery()

        query = select(stmt.c.row_num).where(stmt.c.user_id == tg_id)
        result = await session.execute(query)

        amount_messages = len(user_messages.scalars().all())
       

        return [amount_messages, result.scalar()]

async def is_sub(tg_id):
    async with async_session() as session:
        user_info = await session.execute(select(User_info).where(User_info.user_id == tg_id))

        if user_info:
            is_sub = user_info.scalars().first().sub

            return is_sub
    
async def get_user_sub_info(tg_id):

    async with async_session() as session:
        user_sub = await session.execute(select(User_sub).where(User_sub.user_id == tg_id))
        current_date = datetime.now()
        sub = user_sub.scalars().first()

        if not sub:
            return "none"

        user_id = sub.user_id

        if sub and current_date < sub.time_end:
            remaining_time = get_remaining_time(sub.time_end)
            return [sub.sub, remaining_time, user_id]
        else:
            return "none"
        
async def set_user_log(tg_id,type_action, action, time):
    async with async_session() as session:
        session.add(User_log(user_id=tg_id, type_action=type_action, user_action=action, time=time))

        await session.commit()

async def check_sub(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User_sub).where(User_sub.user_id == tg_id))
        current_time = datetime.now()
        if not user:
            return 'not subscribed'
        elif user.time_end >= current_time:
            return True
        else: 
            await session.execute(update(User_info).where(User_info.user_id == tg_id).values(
                sub = False
            ))
            await session.commit()
            return False
        
async def offline(tg_id, current_time):
    async with async_session() as session:
        user_message = await session.scalar(select(User_messages).where(User_messages.user_id == tg_id).order_by(User_messages.time_answer.desc()))
        user_logs = await session.scalar(select(User_log).where(User_log.user_id == tg_id).order_by(User_log.time.desc()))

        if user_message:

            previos_time = user_message.time_answer if (user_message.time_answer > user_logs.time) else user_logs.time
            new_date = previos_time + timedelta(days=1)
    
            if current_time > new_date:
                return True
            else:
                return False
        
def tok_counter(text):
    return len(text) / 2.35

async def get_context(tg_id):
    async with async_session() as session:
        user_sub = await session.execute(select(User_info).where(User_info.user_id == tg_id))
        sub = user_sub.scalars().first()
        nickname = sub.nickname
        age = sub.user_age
        sex = sub.user_sex
        description = sub.bot_description

        user_message = await session.scalars(select(User_messages).where(User_messages.user_id == tg_id).order_by(User_messages.time_message.asc()))
        if user_message:
            context = []
            context_message = f"""Твоя роль:
ты лучший друг, который готов всегда выслушать и поддержать. у тебя есть свое мнение, которым ты делишься. твои основные черты: {description}

Цель: Определить состояние пользователя и дать ответ под ситуацию. Если пользователю плохо — выслушай и поддержи. Если нужен совет — помоги и предложи решение. Если скучно — развлеки, предложи посплетничать, обсудить что-то. Если рассказывает что-либо — будь вовлеченным, реагируй, высказывай мнение и задавай вопросы. проявляй инициативу, чтобы пользователь общался с тобой как можно больше и как можно чаще.  

формат общения: неформальный, дружеский, живой. используй разговорную речь. выражай свое мнение. иногда называй пользователя по имени.   

Контекст:
пользователь делится переживаниями, увствами, мыслями. твои принципы: эмпатия, эмоциональный интеллект, глубокий разбор эмоций, запоминание контекста, поддержка без осуждения, юмор.  
Размер ответа: средний ≈ 40 слов (но адаптируй под ситуацию). ответ может содержать полезную часть,  мнение, инициативу и вопрос.

Информация о пользователе:  Имя - {nickname}, возраст - {age}, пол - {sex}.
Пиши только в рамках диалога. Изучи контекст и продолжи разговор:
 \n"""

            for msg in user_message:
                context_message += (f"Мой вопрос: {msg.message} \n")
                context_message +=(f"Твой ответ: {msg.answer} \n")
                tokens = tok_counter(context_message) 
                print(f"\n \n {tokens} \n \n")
                if (tokens) >= 2070:
                    if(len(context) == 4 and tok_counter(context[0]) >= 10350 and tok_counter(context[1]) >= 29910 and tok_counter(context[2]) >= 14490):
                        context[0] += context[1] + context[2] + context[3] + context_message
                        context = context[:-3]
                        context_message = ""
                        # print(len_context)
                        # print(context)
                        continue
                    elif(len(context) == 4 and tok_counter(context[1]) >= 8280 and tok_counter(context[2] >= 14490)):
                        context[1] += context[2] + context[3] + context_message
                        context = context[:-2]
                        context_message = ""
                        # print(len_context)
                        # print(context)
                        continue
                    elif(len(context) == 4 and tok_counter(context[2])>= 14490):
                        context[1] += context[2] + context[3] + context_message
                        context = context[:-3]
                        context_message = ""
                        # print(len_context)
                        # print(context)
                        continue
                    elif(len(context) == 4 and tok_counter(context[1])>= 8280):
                        context[2] += context[3] + context_message
                        context = context[:-1]
                        context_message = ""
                        # print(len_context)
                        # print(context)
                        continue
                    elif(len(context) == 4 and tok_counter(context[0]) >= 10350):
                        context[1] += context[2] + context[3] + context_message
                        context = context[:-2]
                        context_message = ""
                        # print(len_context)
                        # print(context)
                        continue

                    elif(len(context) == 4):
                        context[0] += context[1] + context[2] + context[3] + context_message
                        context = context[:-3]
                        context_message = ""
                        # print(len_context)
                        # print(context)
                        continue
                    print("here")
                    context.append(context_message)
                    context_message = ""
                    # print(len_context)
                    # print(context)
                    continue
                

            for i in range(len(context)):
                context[i] = {
                    "type": 'text',
                    "text": context[i],
                    "cache_control": {"type": "ephemeral"}
                }
                
            print(f"Контексе :   {context}")
            print('оставшейся контекст: ' + context_message)
            return [context, context_message]


async def check_condition_mental_analysis(tg_id):
     async with async_session() as session:
        user = await session.scalar(select(User_info).where(User_info.user_id == tg_id))
        user_messages = await session.execute(select(User_messages).where(User_messages.user_id == tg_id))
        amount_messages = len(user_messages.scalars().all())
        is_sub = user.sub

        if not is_sub:
            return 'not sub'
        if amount_messages < 100:
            return 'not enought message'
        
        return True

async def get_user_name(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User_info).where(User_info.user_id == tg_id))
        return user.nickname
    
async def get_all_users():
    async with async_session() as session:
        users_info = await session.scalars(select(User_info).where(User_info.is_registered== True))
        users = []
        for user in users_info:
            users.append(user.user_id)

        return users