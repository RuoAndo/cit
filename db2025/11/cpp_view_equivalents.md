
# C++ equivalents to SQL VIEW

## 1. using alias
```cpp
using FullName = std::string;
FullName name = "Tom Sawyer";
```

## 2. function abstraction
```cpp
struct Actor {
    std::string first;
    std::string last;
};
std::string fullName(const Actor& a) {
    return a.first + " " + a.last;
}
```

## 3. wrapper class
```cpp
class ActorView {
public:
    ActorView(const Actor& a) : actor(a) {}
    std::string fullName() const {
        return actor.first + " " + actor.last;
    }
private:
    const Actor& actor;
};
```

## 4. const reference
```cpp
const std::vector<Actor>& getActors(const std::vector<Actor>& db) {
    return db;
}
```

## 5. transform view
```cpp
std::vector<std::string> names;
std::transform(actors.begin(), actors.end(), std::back_inserter(names),
    [](const Actor& a){
        return a.first + " " + a.last;
    }
);
```

## 6. C++20 ranges
```cpp
auto names = actors
           | std::views::transform([](const Actor& a){
                 return a.first + " " + a.last;
             });
for (auto& n : names) {
    std::cout << n << std::endl;
}
```

## 7. getter as alias
```cpp
struct Film {
    std::string title;
    std::string category;
};
struct FilmView {
    Film f;
    std::string name() const { return f.title; }
    std::string genre() const { return f.category; }
};
```

## 8. LINQ style
```cpp
auto result = from(films)
    .join(categories)
    .select([](auto& f, auto& c){
        return std::make_tuple(f.title, c.name);
    });
```
