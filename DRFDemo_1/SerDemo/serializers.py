# _*_coding:utf-8_*_
from rest_framework import serializers
from .models import Book

book_list = \
    [
        {
            "id": 1,
            "title": "python全栈",
            "w_category": "Python",
            "pub_time": "2019-11-13",
            "publisher_id": {
                "id": 1,
                "title": "机械出版社"
            },
            "author_list": []
        }
    ]


class PublisherSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=32)


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=32)


def my_validate(value):
    if "敏感信息" in value.lower:
        # 如果有敏感信息，这里我们需要抛出异常
        raise serializers.ValidationError("不能含有敏感信息")
    else:
        return value


class BookSerializer1(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=32, validators=[my_validate])
    CHOICES = ((1, 'Python'), (2, 'Go'), (3, 'Linux'))
    category = serializers.ChoiceField(choices=CHOICES,
                                       source='get_category_display',
                                       read_only=True)
    # 这是前端传来的数据
    w_category = serializers.ChoiceField(choices=CHOICES, write_only=True)
    pub_time = serializers.DateField()

    # 使用many=True  声明这是一个外键foreign还是一个Mangtomany的关系
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.IntegerField(write_only=True)
    author = AuthorSerializer(many=True, read_only=True)
    author_list = serializers.ListField(write_only=True)

    def create(self, validated_data):
        book = Book.objects.create(title=validated_data['title'],
                                   category=validated_data['w_category'],
                                   pub_time=validated_data['pub_time'],
                                   publisher_id=validated_data['publisher_id'])
        book.author.add(*validated_data['author_list'])
        return book

    def update(self, instance, validated_data):
        '''
        如果有能找到传来的title等，就拿前台传来的title等
        :param instance: 就是我们后台找到的book_obj
        :param validated_data:
        :return:
        '''
        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.pub_time = validated_data.get('pub_time', instance.pub_time)
        instance.publisher_id = validated_data.get('publisher_id', instance.publisher_id)
        if validated_data.get('author_list'):
            instance.author.set(validated_data['author_list'])
        instance.save()
        return instance

    def validate_title(self, value):
        if "python" not in value.lower():
            raise serializers.ValidationError("标题必须含有Python")
        return value

    def validate(self, attrs):
        if attrs['w_category'] == '1' and attrs['publisher_id'] == 1:
            return attrs
        else:
            # 下面定义一个异常信息
            raise serializers.ValidationError("分类以及标题不符合要求")


class BookSerializer2(serializers.ModelSerializer):
    # 我们想要拿到字段的中文名，我们可以对目录变量重写
    category = serializers.CharField(source='get_category_display')

    publisher = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        authors_query_set = obj.author.all()
        return [{'id': author_obj.id, 'name': author_obj.name} for author_obj in authors_query_set]

    def get_publisher(self, obj):
        # obj 使我们序列化的每一个Book对象
        publisher_obj = obj.publisher
        # 不管我们的publisher（原表的外键）有多复杂，我们只拿下面两个字段
        return {'id': publisher_obj.id,
                'title': publisher_obj.title}

    class Meta:
        model = Book
        # 我们想要拿到下面三个变量可以这样写
        # fields = ['id', 'title', 'pub_time']
        # 我们想要拿到全部的参数，可以这样写
        fields = '__all__'
        # depth = 1  # 我们就可以拿到外键关系的信息
        # 而实际生产有很多的字段，那我们这样定义深度，可以拿到我们想要的数据吗？
        # 所以我们需要自己定义我们想要拿的字段


class BookSerializer(serializers.ModelSerializer):
    category_display = serializers.SerializerMethodField(read_only=True)
    publisher = serializers.SerializerMethodField(read_only=True)
    authors = serializers.SerializerMethodField(read_only=True)

    def get_authors(self, obj):
        authors_query_set = obj.author.all()
        return [{'id': author_obj.id, 'name': author_obj.name} for author_obj in authors_query_set]

    def get_category_display(self, obj):
        return obj.get_category_display()

    def get_publisher(self, obj):
        publisher_obj = obj.publisher
        return {'id': publisher_obj.id,
                'title': publisher_obj.title}

    class Meta:
        model = Book
        fields = '__all__'
        # 我们不想显示不要的字段，如何做呢？
        extra_kwargs = {'category': {'write_only': True},
                        'author': {'write_only': True},
                        'publisher': {'write_only': True}}
