from database.DB_connect import DBConnect


class DAO:

    def __init__(self):
        pass
    @staticmethod
    def getCromosomi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select GeneID, Chromosome
                    from genes
                    where Chromosome > 0
                    group by GeneID, Chromosome"""

        cursor.execute(query)

        for row in cursor:
            result.append((row["Chromosome"], row["GeneID"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArco(crom1, crom2):
        conn = DBConnect.get_connection()

        result = 0.0

        cursor = conn.cursor(dictionary=True)
        query = """select g1.Chromosome, g2.Chromosome, g1.GeneID, g2.GeneID, i.Expression_Corr 
                from genes_small.genes g1, genes_small.genes g2, genes_small.interactions i 
                where (g1.GeneID, g2.GeneID) = (i.GeneID1, i.GeneID2) and g1.Chromosome <> g2.Chromosome
                and g1.Chromosome = %s and g2.Chromosome = %s
                group by g1.GeneID, g2.GeneID"""

        cursor.execute(query, (crom1, crom2, ))

        for row in cursor:
            result += float(row["Expression_Corr"])

        cursor.close()
        conn.close()
        return result
