# GameServer
A simple python UDP GameServer

Start the GameServer with "python3 __init__.py"

Server runs on port 20001 by default (Editable in game_server.py)

Create lobby by sending a UDP Package with the content "create_lobby"

Join a lobby via "join_lobby_i" where "i" is the LobbyID

Send lobby specific packages via "lID_i_command" where "i" is the LobbyID and "command" is the command to execute (must parse in lobby.py -> receivePackage())

