import schedule
import time
from threading import Thread

from jobs.processamento import executar_job
from app.api import app 

running = True

def execute_job():
    schedule.every(1).minutes.do(executar_job)

def run_schedule():
    while running:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    executar_job()

    job_thread = Thread(target=execute_job)
    job_thread.start()

    schedule_thread = Thread(target=run_schedule)
    schedule_thread.start()

    flask_thread = Thread(target=app.run, kwargs={'debug': False})
    flask_thread.start()

    while running:
        user_input = input("Pressione 'q' para sair ")
        if user_input.strip().lower() == 'q':
            running = False
            
    print("Stopping threads...")
    schedule.clear() 
    running = False 
    schedule_thread.join()
    job_thread.join()
    flask_thread.join()
