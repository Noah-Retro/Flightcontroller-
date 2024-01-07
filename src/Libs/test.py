from db_tools import DbHandler
from gui import VisualizationHandler


if __name__ == "__main__":
    db = DbHandler()
    vsh = VisualizationHandler()
    db.storeTestData(100,0.01)
    df = db.load_test_data()
    fig = vsh.plot_3d_coordinates(df).show()
    vsh.plot_2d_path_on_map(df).show()