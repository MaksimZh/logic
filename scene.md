# Защита от потенциальных изменений
Вот функция, которая преобразует дерево виджетов в полигоны с текстурой:

```F#
let rec scene (view: MatrixW, clipping: Rect) (widget: Widget)
        : GLTriangle list =
    let self =
        match widget.Data with
        | :? ImageData as data ->
            let (Image name) = data
            sprites[name] (view, clipping) widget.Location
        | :? TextData as data -> 
            let tmp = textSprites data.Text (view, clipping) widget.Location
            tmp
        | _ -> []
    match widget.Content with
    | None -> self
    | Some container ->
        let clip = clipping.Intersect (widget.Location.Transform view)
        match clip with
        | None -> self
        | Some new_clipping ->
            let translated_view =
                view * (MatrixW.translation widget.Location.LeftBottom)
            let new_view =
                match widget.Data with
                | :? LensData as lens ->
                    let (Lens v) = lens
                    translated_view * v
                | _ -> translated_view
            List.append self (
                container.Children |>
                Seq.map (scene (new_view, new_clipping)) |>
                List.concat)
```

Первое потенциальное место для изменений - выражение для `self`.
Хотя пока трудно придумать что ещё может понадобиться
кроме изображений и текста,
нельзя исключать, что этот код придётся менять снова.
Кроме того, он использует функции с большим количеством аргументов,
что выглядит довольно плохо.

Вторая часть с тремя вложенными `match` выглядит ещё хуже.
К тому же здесь снова возвращаемся к анализу типа поля `widget.Data`,
хотя интуитивно ожидается, что после первого `match`
его уже не будут трогать.

Руки чешутся сделать абстрактный класс `WidgetData` и растащить логику `scene`
по его подклассам, но это как раз то, чего я старался избежать.

Ради гибкости виджеты сделаны легковесными и прозрачными записями (record).
Работа функций с ними напоминает паттерн Visitor -
воздействие происходит извне.
Вместо методов классов используются функции, хранящиеся в полях записей.
Такая архитектура легко модифицируется,
что идеально подходит для первых шагов в программировании GUI
после 20-летнего перерыва.

По замыслу, логика отображения виджетов
должна быть хорошо локализована в `scene`.
Эта функция - уже достаточно низкоуровневый слой -
последний перед OpenGL, и такое точно стоит собрать в одном модуле.

Если присмотреться, тут решается три задачи:
**что**, **где** и **когда** рисовать.
Функция `scene`, прежде всего, отвечает за параметр **когда** -
в каком порядке виджеты отображаются.
За параметр **где** отвечают матрица `view` и прямоугольник `clipping`,
которые путешествую по всем рекурсивным и нерекурсивным вызовам.
Так что это хорошие кандидаты для помещения в отдельный класс.
Параметр **что** - полностью ортогональная логика,
его обработка даже вынесена в отдельный `match`,
который вычисляет значение `self`.

Нужно разделить всё на 3 разных сущности, или больше:

```F#
// Что ----------------------------------------------------

type Sprite =
    {
        Location: Rect
        Texture: Rect
        Palette: float32
    }
    member this.Triangles = [(*TODO*)]


let display (data: obj) (size: Vector) : Sprite list =
    match data with
    | :? ImageData as data ->
        [(*TODO*)]
    | :? TextData as data -> 
        [(*TODO*)]
    | _ -> []


// Где ----------------------------------------------------

type SpriteView (view: MatrixW, clipping: Rect) =
    
    member this.Inner (widget: Widget) : SpriteView option =
        let clip = clipping.Intersect (widget.Location.Transform view)
        match clip with
        | None -> None
        | Some newClipping ->
            let translatedView =
                view * (MatrixW.translation widget.Location.LeftBottom)
            let new_view =
                match widget.Data with
                | :? LensData as lens ->
                    let (Lens v) = lens
                    translatedView * v
                | _ -> translatedView
            Some (SpriteView (new_view, newClipping))

    
    member this.Place (source: Sprite list) : Sprite list =
        [(*TODO*)]


// Когда --------------------------------------------------

let rec scene (view: SpriteView) (widget: Widget)
        : Sprite list =
    match view.Inner widget with
    | None -> []
    | Some innerView ->
        let self = display widget.Data widget.Location.Size |> innerView.Place
        match widget.Content with
        | None -> self
        | Some container ->
            List.append self (
                container.Children |>
                Seq.map (scene innerView) |>
                List.concat)
```

Теперь мы возвращаем спрайты, а не полигоны,
которые появятся на более низком уровне абстракции.

Логика функции `scene` стала прозрачной:
если виджет видно, то показать его самого
и "детей" (во внутренних координатах).

Все вычисления координат ушли в `SpriteView`.
Изменения в логике отображения возникнут здесь, но не затронут `scene`.
Даже если `clipping` перестанет быть прямоугольником -
`scene` этими подробностями не занимается.

Сами спрайты выбираются функцией `display`,
которая получает только размеры области.
Ей не нужно знать где виджет находится и как масштабируется.

Всё это, в каком-то смысле, интерфейсы,
только без ключевого слова `interface`.
