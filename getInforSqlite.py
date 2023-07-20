import sqlite3

FILE_PATH = "datasets/AFLW/aflw.sqlite"

def open_aflw_file(file_path):
    results = []
    conn = sqlite3.connect(file_path)

    cur = conn.cursor()

    SELECT_STRING = """ 
                        faceImages.image_id,
                        faces.file_id,
                        faceImages.filepath,
                        
                        faces.face_id,

                        featureCoords.feature_id,
                        featureCoords.x,
                        featureCoords.y,
                    
                        faceRect.x,
                        faceRect.y,
                        faceRect.w,
                        faceRect.h
                    """
    FROM_STRING = "faceImages, faceRect, faces, featureCoords"

    WHERE_STRING =  """ 
                        faceImages.file_id = faces.file_id 
                    AND faces.face_id = featureCoords.face_id
                    AND featureCoords.face_id = faceRect.face_id
                    """
    QUERY_STRING = f"""
                        SELECT {SELECT_STRING}
                        FROM {FROM_STRING}
                        WHERE {WHERE_STRING}
                """

    db = cur.execute(QUERY_STRING)
    # print(len(db))
    face_id = []
    print("done")
    # count = 0
    for row in db:
        # print(row[2])
        if int(row[2].split("/")[0]) == 0:
            # count += 1
            # print(count)
            if row[3] not in face_id:
                tmp = {}
                tmp["file_id"] = row[1]
                tmp["file_path"] = row[2]
                tmp["face_id"] = row[3]
                face_id.append(row[3])
                box = [row[7], row[8], row[9], row[10]]
                tmp['bbox'] = box

                tmp['feature_id'] = []
                tmp['feature_id'].append(row[4])
                tmp['feature_coords'] = []
                tmp['feature_coords'].append((row[5], row[6]))

                results.append(tmp)
            else:
                tmp = get_information(results, row[3])
                tmp["feature_id"].append(row[4])
                tmp["feature_coords"].append((row[5], row[6]))

    return results

def get_information(results, face_id):
    for res in results:
        if res["face_id"] == face_id:
            return res

if __name__ == "__main__":
    test = open_aflw_file(FILE_PATH)
    print(test[0])