from rest_framework import serializers
from polls.models import Poll, Choice


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('id', 'text', 'votes')
        read_only_fields = ('votes',)


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('id', 'uid', 'text', 'pub_date', 'choices')
        read_only_fields = ('id', 'uid', 'pub_date')

    def validate(self, data):
        if len(data['choices']) < 2:
            raise serializers.ValidationError('Need at least two choices')
        return data

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(poll=poll, **choice_data)
        return poll
