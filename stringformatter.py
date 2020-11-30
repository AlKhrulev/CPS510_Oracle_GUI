createTablesString = (open("createTables.txt", "r").read().split('\n'))
for x in createTablesString:
    print(x)