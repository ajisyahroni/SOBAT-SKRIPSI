<template>
  <div class="center-container">
    <v-card
      elevation="0"
      class="pa-5 d-flex flex-column"
      width="1163"
      height="875"
    >
      <!-- HEADER -->
      <div class="d-flex justify-center">
        <div style="width: 210px">
          <v-select
            background-color="blue-grey lighten-5"
            solo
            flat
            dense
            class="font-abhaya font-weight-bold"
            v-model="selectedSubfield"
            :items="subfields"
            item-text="name"
            item-value="code"
          />
        </div>
      </div>
      <!-- END HEADER -->
      <!-- CONTENT -->

      <!-- CHART -->
      <div id="chart">
        <apexchart
          type="bar"
          height="430"
          :options="chartOptions"
          :series="series"
        ></apexchart>
      </div>
      <!-- END CHART -->

      <!-- TABLE -->
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Year</th>
              <th class="text-left">Most Topic</th>
              <th class="text-left">Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="data in tableData" :key="data.year">
              <td>{{ data.year }}</td>
              <td>{{ data.topic }}</td>
              <td>{{ data.total }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
      <!-- END TABLE  -->

      <!-- END CONTENT -->
    </v-card>
  </div>
</template>

<script>
import { API_URL } from "../api";
export default {
  data: () => ({
    // table data
    tableData: [],

    // pie data
    series: [],
    chartOptions: {
      chart: {
        type: "bar",
        height: 430,
      },
      plotOptions: {
        bar: {
          horizontal: true,
          dataLabels: {
            position: "top",
          },
        },
      },
      dataLabels: {
        enabled: true,
        offsetX: -6,
        style: {
          fontSize: "12px",
          colors: ["#fff"],
        },
      },
      stroke: {
        show: true,
        width: 1,
        colors: ["#fff"],
      },
      tooltip: {
        shared: true,
        intersect: false,
      },
      xaxis: {
        categories: [2019, 2020, 2021],
      },
    },

    // single value
    selectedSubfield: "SE",
    subfields: [
      {
        code: "SE",
        name: "Software Engineering",
      },
      {
        code: "MM",
        name: "Multimedia",
      },
      {
        code: "CN",
        name: "Computer Network",
      },
    ],
  }),

  watch: {
    selectedSubfield(code) {
      this.loadSummary(code);
    },
  },

  mounted() {
    this.loadSummary(this.selectedSubfield);
  },

  methods: {
    loadSummary(code) {
      let url = `${API_URL}/summary-result?subfield=${code}`;
      fetch(url)
        .then((r) => r.json())
        .then((it) => {
          // mapping chart response
          let chart = Object.entries(it?.data?.chart);
          let series = chart.map((v) => ({
            name: v[0],
            data: Object.values(v[1]),
          }));
          this.series = series;

          // mapping best topic response
          let table = it?.data?.best_topic;
          this.tableData = table;
        });
    },
  },
};
</script>

<style scoped>
.center-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>