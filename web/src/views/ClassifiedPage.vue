<template>
  <div class="center-container">
    <v-card
      elevation="0"
      class="pa-12 d-flex flex-column"
      width="70%"
      height="875"
      style="overflow-y: scroll"
    >
      <!-- HEADER -->
      <div class="d-flex justify-space-between flex-wrap">
        <div style="height: 50px">
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

        <div style="height: 34px" class="d-flex align-center font-abhaya">
          <v-btn
            @click="setYear(2019)"
            v-bind="
              selectedYear == 2019
                ? activePeriodeBtnAttr
                : nonactivePeriodeBtnAttr
            "
          >
            2019
          </v-btn>
          <hr style="width: 50px" />
          <v-btn
            @click="setYear(2020)"
            v-bind="
              selectedYear == 2020
                ? activePeriodeBtnAttr
                : nonactivePeriodeBtnAttr
            "
            >2020</v-btn
          >
          <hr style="width: 50px" />
          <v-btn
            @click="setYear(2021)"
            v-bind="
              selectedYear == 2021
                ? activePeriodeBtnAttr
                : nonactivePeriodeBtnAttr
            "
            >2021</v-btn
          >
        </div>
      </div>
      <!-- END HEADER -->

      <!-- CONTENT -->
      <v-row class="mt-10">
        <v-col
          cols="12"
          md="12"
          xl="8"
          order-sm="1"
          order-md="1"
          order-lg="0"
          order-xl="0"
        >
          <div>
            <!-- LABELS -->
            <v-btn
              :color="selectedTopic == label.code ? '#E1C4B6' : ''"
              @click="setLabel(label.code)"
              class="mr-2 font-abhaya font-weight-bold text-capitalize"
              v-for="label in labels"
              :key="label.id"
              depressed
            >
              {{ label.name }}
            </v-btn>
            <!-- END LABELS -->

            <!-- DOCS LIST-->
            <ol
              class="font-quicksand mt-5"
              style="
                line-height: 182.5%;
                height: 500px;
                overflow-y: scroll;
                cursor: pointer;
              "
            >
              <li
                @click="openThesisDialog(doc.eprintid)"
                v-ripple
                v-for="doc in docs"
                :key="doc.eprintid"
                class="text-lowercase"
              >
                {{ doc.title }}
              </li>
            </ol>
            <!-- END DOC LIST -->
          </div>
        </v-col>
        <v-col>
          <!-- CHART -->
          <div id="chart">
            <apexchart
              type="donut"
              :options="chartOptions"
              :series="series"
            ></apexchart>
            <!-- END CHART -->
          </div>
        </v-col>
      </v-row>
      <!-- END CONTENT -->

      <!-- ACTION CARDS -->
      <v-card-actions class="d-flex justify-center">
        <v-btn
          :to="{ name: 'SummaryPage' }"
          color="#6898AC"
          tile
          depressed
          dark
          class="font-abhaya font-weight-bold text-lowercase px-5 py-2"
        >
          summary
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import ThesisDetail from "../components/ThesisDetail.vue";
import { API_URL } from "../api";
export default {
  data: () => ({
    // PIE DATA
    series: [90, 55, 41, 17, 15],
    chartOptions: {
      labels: [],
      chart: {
        type: "donut",
      },
      responsive: [
        {
          breakpoint: 480,
          options: {
            chart: {
              width: 200,
            },
            legend: {
              position: "bottom",
            },
          },
        },
      ],
    },

    // single value
    selectedTopic: "SE_AI",
    selectedSubfield: "SE",
    selectedYear: 2019,

    // btn periode attrs
    activePeriodeBtnAttr: {
      depressed: true,
      color: "#E1C4B6",
      rounded: true,
      dark: true,
    },
    nonactivePeriodeBtnAttr: {
      text: true,
    },

    // lists
    labels: [],
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
    docs: [],
  }),

  mounted() {
    this.loadData("SE", 2019, "SE_AI");
  },

  watch: {
    selectedSubfield(code) {
      this.loadData(code, this.selectedYear, 1);
    },
  },

  methods: {
    async loadData(subfield, year, topic) {
      const url = `${API_URL}/classify-result?subfield=${subfield}&year=${year}&topic=${topic}`;
      fetch(url)
        .then((r) => r.json())
        .then((it) => {
          this.docs = it?.data?.theses;
          this.labels = it?.data?.available_topics;

          // set chart data
          console.log(it?.data?.chart);
          this.series = Object.values(it?.data?.chart);
          this.chartOptions = {
            ...this.chartOptions,
            ...{ labels: Object.keys(it?.data?.chart) },
          };

          // set attribute
          this.selectedTopic = it?.query?.topic;
          this.selectedYear = it?.query?.year;
          this.selectedSubfield = it?.query?.subfield;
        });
    },

    openThesisDialog(eprintid) {
      fetch(
        `${API_URL}/thesis-detail?eprintid=${eprintid}&subfield=${this.selectedSubfield}`
      )
        .then((r) => r.json())
        .then((it) => {
          let detail = {
            title: it?.data?.title,
            abstract: it?.data?.abstract,
            year: it?.data?.year,
            uri: it?.data?.uri,
          };
          this.$dialog.open(ThesisDetail, {
            props: { detail },
            width: "70%",
          });
        });
    },

    setYear(year) {
      this.loadData(this.selectedSubfield, year, this.selectedTopic);
    },
    setLabel(code) {
      this.loadData(this.selectedSubfield, this.selectedYear, code);
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