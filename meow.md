```Java
class Animal {
    public void makeSound() {
        System.out.println("Some generic animal sound");
    }
}

class Cat extends Animal {

    @Override
    public void makeSound() {
        System.out.println("Meow");
    }
}

public class Main {
    public static void main(String[] args) {
        Animal cat = new Cat();
        cat.makeSound();
    }
}
```

Здесь будет вызван метод потомка.
Если убрать `@Override`, то тут возможны варианты.

1. Самый лучший вариант - ошибка компиляции,
поскольку такой метод уже есть и мы не выразили намерение его переопределять.
2. Средний вариант - переопределение по умолчанию.
Тогда, поскольку мы создали экземпляр класса `Cat`,
будет вызван метод потомка.
3. Худший вариант - два метода: старый для суперкласса и новый для потомка.
Тогда, поскольку мы задали для `cat` тип суперкласс, будет вызван его метод,
а намерение, скорее всего, совсем другое.

В Python работает вариант 2. В Java, надеюсь, вариант 1.
