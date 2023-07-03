# async with async_session_maker() as session:
#     stmt = select(User)
#     response = await session.execute(stmt)
#     result = response.all()[0]
#     assert len(result) == 1, 'Not right number of users was created'
#     user = result[0]
#     assert user.email == "s@s.com", 'Email created is wrong'
#     assert user.username == "string", "Username created is wrong"
