# NewRelic dependency graph

This tool draws a complete dependency graph based on data available in NewRelic. Similar to the [Service Maps feature](https://docs.newrelic.com/docs/using-new-relic/service-maps), but as a static DOT graph (plotted to PDF, PNG, whatever).

The script uses an undocumented HTTP endpoint in NewRelic's APM/RPM product to get tracing data and Graphviz to plot it.

Go ahead and give it a spin:

    docker-compose build
    docker-compose run --rm dependencygraph
    open out/graph.pdf

It will ask for your personal NewRelic credentials (email and password), as the specific NewRelic endpoint used by this script cannot be authed via an API key/access token.

Have fun!
