a
    G$)b�  �                   @   s�   d dl Z d dlmZ d dlZe� Zdd� Zdd� Zdd� Zd	d
� Zdd� Z	dd� Z
dd� Zdd� Zdd� Zdd� Zdd� Zedkr�ee
d�� dS )�    N)�IMDbc                 C   sX   t �| �}g }|d j}t �|�}|d d }|dd � �d�}|d }d|� d�| S )Nr   z
box officezCumulative Worldwide Gross�   z, zWorldwide Gross of z is: )�ia�search_movie�movieID�	get_movie�split)�filmName�movieZ
gross_list�idZgrossZ	gross_numZgross_number� r   �-/Users/brandonhoge/MovieGenie-1/imdb_actor.py�
movieGross   s    


r   c                 C   s   t � }|�| �}|d j}|S )Nr   )r   Zsearch_person�personID)�namer   �personZ	person_idr   r   r   r      s    

r   c           	      C   sh   t � }d}|�| �}t|d �}g }|�� D ]6}||v r,|dd� �d�}t|�|��}|�|� q,|S )Nzid:�actor�   �   �[)r   Z
get_person�strr   �stripr   �append)	r   r   �word2Z
actor_name�xZnew_list�wordZmovie_IDZmovie_titler   r   r   �get_actor_movies$   s    
r   c                 C   s6   g }| D ](}zt |�}|�|� W q   Y q0 q|S )N)r   r   )Z
movie_listZgross_actorr
   r   r   r   r   �actor_movie_gross3   s    r   c                   C   s   t ��  t dd � S )N�����)r   �sortr   r   r   r   �gross_actor_average?   s    r    c                 C   s  ddddddddd	d
ddd�}t �| �}|d j}t �|�}t �|d� |d }|d }t|�D ]B\}}|�� }	|	d }
|
�d�d }|dkr�|| } q�|d7 }q`t|� |�� }|d }|�d�d }|d }|d }|D ]}||kr�|| }q�|d | d | S )NZ01Z02Z03Z04Z05Z06Z07Z08Z09�10�11Z12)�January�FebruaryZMarchZApril�MayZJuneZJulyZAugustZ	SeptemberZOctoberZNovemberZDecemberr   zrelease datesz::ZUSAr   �   �-)r   r   r   r   �update�	enumerater   �print)r	   Zlist_of_monthsr
   r   �movie1�dateZ
movie_date�count�iZ
temp_date1Z
temp_date2ZcountryZdate2�dayZ
reddit_dayZreddit_monthZreddit_year�monthr   r   r   �get_dateD   sJ    �




r1   c                 C   sD   | dkrdS | dk r | dkr dS | dk r4| dkr4dS | dk r@dS d S )N�   �Ar   �Br&   �C�Dr   )r-   r   r   r   �
actor_tierr   s    r7   c                  C   s4   g } t �� }td�D ]}|| d }| �|� q| S )N��   �title)r   Zget_top250_movies�ranger   )�
title_list�searchr.   r   r   r   r   �get_top_movies}   s    r=   c                 C   s�   g }g }| D ]f}t �|�}|d j}t �|�}|�|d d � |r|�d�}d}|d |� D ]}	|�|	d � q^q|D ]}t|��� }
|�|
� qx|S )Nr   r9   �cast�   r   )r   r   r   r   r   �getr   �lower)r;   Zactor_movie_strZ	test_listr.   r+   r   r
   r>   Z	topActorsr   Zlower1r   r   r   �get_top_movie_cast�   s     



rB   c                 C   s|   d}d}t dddd��R}t�|�}| D ]*}| ||� }|�|� |d7 }|d7 }q&|��  W d   � n1 sn0    Y  d S )Nr   �	   �list_updated.csv�w� )�newline)�open�csv�writer�writerow�close)�list�startZfinishZfile1rJ   r.   Zlist1r   r   r   �write_list_file�   s    


rO   c                 C   s^   d}t d��>}tj|dd�}|D ]}| j | |v r |d7 }q W d   � n1 sP0    Y  |S )Nr   rD   �,)�	delimiterr   )rH   rI   �readerrA   )r   r-   Zfile2Z	csvreader�rowr   r   r   �search_list_actor�   s    
(rT   �__main__ZDune)rI   Zimdbr   �rer   r   r   r   r   r    r1   r7   r=   rB   rO   rT   �__name__r*   r   r   r   r   �<module>   s    .
