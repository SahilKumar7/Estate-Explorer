import "./listPage.scss";
import Filter from "../../components/filter/Filter";
import Card from "../../components/card/Card";
import Map from "../../components/map/Map";
import Loader from "../../components/loader/Loader";
import EmptyState from "../../components/emptyState/EmptyState";
import { Await, useLoaderData } from "react-router-dom";
import { Suspense } from "react";

function ListPage() {
  const data = useLoaderData();

  return (
    <div className="listPage">
      <div className="listContainer">
        <div className="wrapper">
          <Filter />
          <Suspense fallback={<Loader />}>
            <Await
              resolve={data.postResponse}
              errorElement={<EmptyState message="Could not load properties. Please try again." />}
            >
              {(postResponse) =>
                postResponse.data.length === 0 ? (
                  <EmptyState message="No properties match your search." />
                ) : (
                  <div className="cardGrid">
                    {postResponse.data.map((post) => (
                      <Card key={post.id} item={post} />
                    ))}
                  </div>
                )
              }
            </Await>
          </Suspense>
        </div>
      </div>
      <div className="mapContainer">
        <Suspense fallback={<Loader />}>
          <Await
            resolve={data.postResponse}
            errorElement={<EmptyState message="Map unavailable." />}
          >
            {(postResponse) => <Map items={postResponse.data} />}
          </Await>
        </Suspense>
      </div>
    </div>
  );
}

export default ListPage;
