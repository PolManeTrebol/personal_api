def __find_id_by_path(self, data, target_path, target_name):
    for item in data:
        if item['path'] == target_path and item['name'] == target_name:
            return item['id']
        # Si el elemento tiene subgrupos, aplicamos la recursividad
        if 'subGroups' in item:
            result = self.__find_id_by_path(item['subGroups'], target_path, target_name)
            if result:
                return result
    return None  # Si no encontramos nada, retornamos None
