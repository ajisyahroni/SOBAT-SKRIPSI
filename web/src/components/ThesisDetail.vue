<template>
  <div>
    <v-card :rounded="0" class="px-5">
      <v-card-text class="px-5">
        <!-- HEADER -->
        <!--  -->
        <!--  -->
        <div class="d-flex justify-space-between font-abhaya">
          <div class="d-flex flex-column">
            <h2 class="mt-4">
              {{ detail.title }}
            </h2>

            <!-- LABELS -->
            <div class="d-flex mt-2">
              <div
                class="font-abhaya text-capitalize px-2"
                style="border-radius: 3px; background-color: #f5f5f5"
              >
                Label
              </div>
            </div>
          </div>
        </div>

        <v-divider class="my-5" />

        <div
          class="font-abhaya mt-5"
          style="line-height: 182.5%; font-size: 14pt"
        >
          {{ detail.abstract }}
        </div>

        <v-card-actions class="d-flex justify-end mt-5">
          <v-btn
            class="font-abhaya font-weight-bold text-lowercase px-5 py-2"
            text
            @click="$dialog.close()"
          >
            tutup
          </v-btn>
          <v-btn
            color="#6898AC"
            tile
            depressed
            dark
            class="font-abhaya font-weight-bold text-lowercase px-5 py-2"
            :href="detail.uri"
            target="_blank"
          >
            visit on eprints
          </v-btn>
        </v-card-actions>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  props: ["detail"],
};
</script>

<style>
</style>