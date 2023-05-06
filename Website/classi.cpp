#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <cmath>
#include "json.hpp"

using json = nlohmann::json;

// A struct to hold polygon coordinates and the corresponding GEOID
struct Polygon {
    std::vector<std::pair<double, double>> coordinates;
    std::string geoid;
};

// Function to check if a point (given by lon and lat) is inside a polygon
bool pointInsidePolygon(const std::vector<std::pair<double, double>>& polygon, double lon, double lat) {
    int i, j, nvert = polygon.size();
    bool inside = false;

    for (i = 0, j = nvert - 1; i < nvert; j = i++) {
        if (((polygon[i].second > lat) != (polygon[j].second > lat)) &&
            (lon < (polygon[j].first - polygon[i].first) * (lat - polygon[i].second) / (polygon[j].second - polygon[i].second) + polygon[i].first)) {
            inside = !inside;
        }
    }

    return inside;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <longitude> <latitude>" << std::endl;
        return 1;
    }

    double lon = std::stod(argv[1]);
    double lat = std::stod(argv[2]);

    // Read in the GeoJSON file
    std::ifstream geojsonFile("C:\\Users\\pjrio\\tl_2020_05_bg\\shape2geojson.geojson");
    if (!geojsonFile.is_open()) {
        std::cerr << "Failed to open GeoJSON file." << std::endl;
        return 1;
    }

    json geojsonData;
    geojsonFile >> geojsonData;

    // Extract the polygons from the GeoJSON data along with the corresponding GEOIDs
    std::vector<Polygon> polygons;
    for (auto& feature : geojsonData["features"]) {
        auto geometryType = feature["geometry"]["type"].get<std::string>();
        if (geometryType != "Polygon") {
            continue;
        }

        Polygon polygon;
        polygon.geoid = feature["properties"]["GEOID"].get<std::string>();
        for (auto& coordinate : feature["geometry"]["coordinates"][0]) {
            double lon = coordinate[0].get<double>();
            double lat = coordinate[1].get<double>();
            polygon.coordinates.push_back(std::make_pair(lon, lat));
        }

        polygons.push_back(polygon);
    }

    // Check whether the point intersects with any of the polygons
    std::string intersectingGeoid;
    for (auto& polygon : polygons) {
        if (pointInsidePolygon(polygon.coordinates, lon, lat)) {
            intersectingGeoid = polygon.geoid;
            break;
        }
    }

    if (!intersectingGeoid.empty()) {
        std::cout << "The point intersects with polygon GEOID: " << intersectingGeoid << std::endl;
    } else {
        std::cout << "The point does not intersect with any polygons." << std::endl;
    }

}
