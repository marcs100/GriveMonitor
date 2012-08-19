from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
import subprocess

#Note: currently we do not check remote drive periodically for changes

class SystemTray(QSystemTrayIcon):

    """ Creates our System Tray icon and calls our worker to get new data """
    def __init__(self, icon, parent=None):
        
        self.GooglePath = "/home/marc/GoogleDrive"
        
        os.chdir(self.GooglePath)
        
        QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip("Google Drive Sync (Grive)")

        #setup the menu
        menu = QMenu(parent)
        updateAction = menu.addAction("Sync Now")
        exitAction = menu.addAction("Quit")
        QObject.connect(updateAction, SIGNAL("triggered()"), self.ChangeDetected)
        QObject.connect(exitAction, SIGNAL("triggered()"), qApp, SLOT("quit()"))
        self.setContextMenu(menu)
        self.watcher=QFileSystemWatcher(self)
        self.__InitFileWatcher()
        self.__SyncGoogleDrive() #always sync on startup as new files may have been added to remote
        self.show()
        
    #def setQApp(self,app):
    #    self.qapp = app # set to instance of this QApplication
        
    #Initialise the file system watcher   
    def __InitFileWatcher(self):
        self.watcher.addPath(self.GooglePath)
        self.__AddPaths(self.GooglePath,self.watcher) # Add each folder in the directory etc..
        QObject.connect(self.watcher,SIGNAL("directoryChanged(QString)"),self.ChangeDetected)
    
    
    #walk through directories adding paths to QFileSystemWatcher (recursive funtion)    
    def __AddPaths(self,topLevelPath,watcher):
        for root, dirs, files in os.walk(topLevelPath):
            for directory in dirs:
                print("Watching %s/%s"%(root,directory))
                watcher.addPath(root+"/"+directory)
    
        
           
    #slot for QFileSystemWatcher
    def ChangeDetected(self):
        self.__SyncGoogleDrive()
        
    # Sync google drive - (calls grive)
    def __SyncGoogleDrive(self,parent=None):
        #try:
        self.showMessage("Grive","Syncing Your Google Drive",QSystemTrayIcon.Information,4000)
        #self.qapp.processEvents() #otherwise we will not see above message
            
        #stop watching folders when Grive is running
        watchedPaths = self.watcher.directories()
        self.watcher.removePaths(watchedPaths)
            
        returnValue = subprocess.check_call(["./grive"],stderr=None,shell=False)
        if returnValue==0:
            self.showMessage("Grive","Sync completed",QSystemTrayIcon.Information,4000)
        else:
            self.showMessage("Grive","Error - %i returned"%returnValue,QSystemTrayIcon.Warning,7000)
        self.__InitFileWatcher() #start file watcher again now sync has finished 
        #except:
            #self.showMessage("Grive","ERROR - EXCEPTION CAUGHT!",QSystemTrayIcon.Critical,10000)
            #self.qapp.quit()