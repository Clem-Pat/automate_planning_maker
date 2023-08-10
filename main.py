import Tkinter_Manager.tkinter_window as tkinter_window

if __name__ == '__main__':
    app = tkinter_window.Tkinter_window('main')
    while not(app.destroyed) :
        try: app.refresh()
        except: app.destroyed = True

        if app.buttons[1].state == 'clicked':
            app.buttons[1].state = 'unclicked'
            crens = tkinter_window.Tkinter_window('crens', main_app=app)
            while not(crens.destroyed) :
                try: crens.refresh()
                except: crens.destroyed = True

        if app.buttons[2].state == 'clicked':
            app.buttons[2].state = 'unclicked'
            resu = tkinter_window.Tkinter_window('resu', main_app=app)
            while not (resu.destroyed):
                try: resu.refresh()
                except: resu.destroyed = True


"""
issues and things to improve : 
    - faire une légende ds excel
    - lors de leur création les fichiers excels ne se suppriment pas
"""
