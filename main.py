import pandas as pd


items_ids = [
    12303, 12314, 14499, 14510, 14796, 14799, 14897, 15406, 15410, 15701,
    15707, 15708, 41116, 41118, 41120, 41122, 41124, 41210, 41212, 41214,
    41306, 41308, 41310, 41312, 41314, 41412, 41414, 72496, 75904, 75909,
    75934, 75942, 84817, 84819, 88785,
]
items = pd.read_excel(
        "./Данные поставщика.xlsx",
        usecols=["Код артикула", "Название"],
    )
categories = pd.read_excel(
    "./Дерево категорий.xlsx",
    usecols=["cat_id", "cat_3"],
)


def form_tuples_with_id_and_title(item_id: int) -> tuple[int, str]:
    for _, row in items.iterrows():
        if row["Код артикула"] == item_id:
            return row["Код артикула"], row["Название"]
    return item_id, "Unknown"


def get_category_id_by_item_id_and_title(
    id_with_titles_tuple: tuple[int, str]
) -> tuple[int, int | str]:
    for _, row in categories.iterrows():
        if row["cat_3"] in id_with_titles_tuple[1]:
            return id_with_titles_tuple[0], row["cat_id"]
    return id_with_titles_tuple[0], "Unknown"


def main(items_ids: list[int]):
    items_ids_with_titles_tuples = [
        form_tuples_with_id_and_title(item_id) for item_id in items_ids
    ]
    items_ids_with_categories_ids = [
        get_category_id_by_item_id_and_title(item)
        for item in items_ids_with_titles_tuples
    ]
    result = pd.DataFrame(
        items_ids_with_categories_ids, columns=["item_id", "cat_id"]
    )
    result.to_excel("./result.xlsx", index=False)


if __name__ == "__main__":
    main(items_ids)
