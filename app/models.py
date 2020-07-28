from django.db import models
from datetime import date
from django.urls import reverse

class Tag(models.Model):
    name_options = [('array','Array'),('hash table','Hash Table'),('Linked list','Linked list'),('math','Math'),('two pointers','Two Pointers'),('string','String'),('binary search','Binary Search'), ('divide and coquer','Divide and coquer'),('dynamic programming','Dynamic Programming'),('backtracking','Backtracking'),('Stack','stack'),('heap','Heap'),('greedy','Greedy'),('sort','Sort'),('bit manipulation','Bit Manipulation'),('tree','Tree'),('depth first search','DFS'),('breadth first search','BFS'),('union find','Union Find'),('graph','Graph'),('design','Design'),('tpological sort','Topological Sort'),('trie','Trie'),('binary search tree','Binary search tree'), ('queue','Queue')]
    name = models.CharField('Name',max_length=20, choices=name_options, unique=True)

    def __str__(self):
        return self.name.title()


class Problem(models.Model):
    acceptance = models.IntegerField(null=True,blank=True)
    name = models.CharField('Name',max_length=50, unique=True)
    url = models.URLField('URL',max_length=80, null=True, blank=True)
    difficulty_choices = [('easy','Easy'),('medium','Medium'),('hard','Hard')]
    difficulty = models.CharField('Difficulty',max_length= 10, choices=difficulty_choices)
    description = models.TextField('Description')
    tags = models.ManyToManyField(Tag)
    #resolution = models.ForeignKey(ProblemResolution, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def contain_tag(self, aTag):
        return aTag in self.tags

    def style_by_difficulty(self):
        if self.difficulty == 'easy':
            return 'table-success'
        elif self.difficulty == 'medium':
            return 'table-warning'
        else:
            return 'table-danger'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

class ProblemResolution(models.Model):
    date_0 = models.DateField("Date", default=date.today())
    solution_code = models.TextField("Solution")
    big_oh_choices = [('constant','C'),('logarithmic','log'),('linear','N'),('logarithmicN','logN'),('quadratic','N^2'),('cubic','N^3')]
    big_oh = models.CharField('Time complexity(big-oh)',max_length=20, choices=big_oh_choices)
    description = models.TextField('Approach', null=True, blank=True)
    language_code = models.CharField('Language code', max_length=10)
    problem = models.ForeignKey(Problem,null=True,on_delete=models.CASCADE)

    def in_last_month(self):
        return self.date_0.month == date.today().in_last_month
