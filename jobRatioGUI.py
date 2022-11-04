from tkinter import *

window = Tk()
window.title('Job Ratios')
window.config(width=1500, height=900, padx=100, pady=50)

job_number = Label(text='21074')
job_number.grid(row=2, column=0)

job_name = Label(text='Project Abby - Ontario')
job_name.grid(row=2, column=1)

journey_to_apprentice_title = Label(text='Journey to Apprentice Ratio')
journey_to_apprentice_title.grid(row=1, column=2)
set_journey_to_apprentice_ratio = Entry()
set_journey_to_apprentice_ratio.grid(row=2, column=2)

male_to_female_title = Label(text='Male to Female Ratio')
male_to_female_title.grid(row=1, column=3)
set_male_to_female_ratio = Entry()
set_male_to_female_ratio.grid(row=2, column=3)

min_female_count = Label(text='Min Female Count')
min_female_count.grid(row=1, column=4)
set_min_female_count = Entry()
set_min_female_count.grid(row=2, column=4)

journey_to_apprentice_ratio = Label(text='5:1')

window.mainloop()
