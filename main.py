import Tkinter_Manager.tkinter_window as tkinter_window

if __name__ == '__main__':
    app = tkinter_window.Tkinter_window('main')
    while not (app.destroyed):
        try:
            app.refresh()
        except:
            app.destroyed = True

        if app.open_window.cren == True:
            app.open_window.cren = False
            crens = tkinter_window.Tkinter_window('crens', main_app=app)
            while not (crens.destroyed):
                try:
                    crens.refresh()
                except:
                    crens.destroyed = True

        if app.open_window.resu == True:
            app.open_window.resu = False
            resu = tkinter_window.Tkinter_window('resu', main_app=app)
            while not (resu.destroyed):
                if app.open_window.choose_receivers == True:
                    app.open_window.choose_receivers = False
                    choose_receivers = tkinter_window.Tkinter_window('choose_receivers', main_app=app, parent_app=resu)
                    while not (choose_receivers.destroyed):
                        try:
                            choose_receivers.refresh()
                        except:
                            choose_receivers.destroyed = True

                try:
                    resu.refresh()
                except:
                    resu.destroyed = True

"""
issues and things to improve : 
    - Faire en sorte que l'utilisateur puisse importer un planning déjà créé
        PB : Avec autant de créneaux, le planning peut ne pas trouver de personne disponible. Les remplacer par des 'None' pour éviter l'erreur list index out of range
"""
