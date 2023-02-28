from django import forms

class CategoryMC(forms.ModelMultipleChoiceField):
    def label_from_instance(self, category):
        return category.name