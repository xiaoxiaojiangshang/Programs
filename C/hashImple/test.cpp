/*
    Author: jgz
    Date: 2018/7/12 20:23:37
*/

#include <stdio.h>
#include <stdlib.h>
#include "HashTable.c"

// Ҫ�����ϣ���еĽṹ��
struct Student
{
    int age;
    float score;
    char name[32];
    char data[1024 * 1024* 10];
};

// �ṹ���ڴ��ͷź���
static void free_student(void* stu)
{
    free(stu);
}

// ��ʾѧ����Ϣ�ĺ���
static void show_student(struct Student* p)
{
    printf("����:%s, ����:%d, ѧ��:%.2f\n", p->name, p->age, p->score);
}

int main()
{
    // �½�һ��HashTableʵ��
    HashTable* ht = hash_table_new();
    if (NULL == ht) {
        return -1;
    }

    // ���ϣ���м�����ѧ���ṹ��
    for (int i = 0; i < 100; i++) {
        struct Student * stu = (struct Student*)malloc(sizeof(struct Student));
        stu->age = 18 + rand()%5;
        stu->score = 50.0f + rand() % 100;
        sprintf(stu->name, "ͬѧ%d", i);
        hash_table_put2(ht, stu->name, stu, free_student);
    }

    // ����ѧ����������ѧ���ṹ
    for (int i = 0; i < 100; i++) {
        char name[32];
        sprintf(name, "ͬѧ%d", i);
        struct Student * stu = (struct Student*)hash_table_get(ht, name);
        show_student(stu);
    }
    // ���ٹ�ϣ��ʵ��
    hash_table_delete(ht);
    return 0;
}


