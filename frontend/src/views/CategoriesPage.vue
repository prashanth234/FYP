<template>
  <ion-page>
    <ion-content class="ion-padding">
      
      <!-- <p class="page-heading">Explore Your Interests</p> -->

      <div class="grid-container">

				<div
					class="grid-item cpointer hover"
					v-for="(cat, index) in category.categories"
					:key="index"
					@click="openCategory(cat)"
				>

					<ion-img class="cat-image" :src="cat.image" :alt="cat.description">
					</ion-img>

					<div class="cat-title">
						{{cat.name}}
					</div>

					<div class="cat-description" :title="cat.description">
						{{cat.description}}
					</div>

				</div>

      </div>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { useCategoryStore } from '@/stores/category';
import { IonPage, IonContent, IonImg, useIonRouter  } from '@ionic/vue';
import { categoryType } from '@/utils/interfaces'
import { scrollTop } from '@/composables/scroll'

scrollTop()

const ionRouter = useIonRouter();
const category = useCategoryStore();

// category.getCategories()

function openCategory (category: categoryType) {
  ionRouter.push(`interests/${category.id}/posts`)
}

</script>

<style scoped>
.page-heading {
  margin: 0px;
  font-size: 23px;
  font-weight: 500;
  margin-bottom: 10px;
  margin-left: 5px;
	color: var(--ion-color-dark-tint);
}
.grid-container {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
	grid-gap: 20px;
	/* Ensure all rows have the same height */
	grid-auto-rows: auto;
	padding: 5px;
}
.grid-item {
  border: 1px solid var(--ion-color-light-shade);
	color: var(--ion-text-color);
	border-radius: 10px;
	padding: 20px;
	display: flex;
	flex-direction: column;
	text-align: center;
	background: var(--ion-card-background);
}
.cat-image::part(image), .cat-image {
  max-width: 100%;
	max-height: 220px;
  object-fit: cover;
	border-radius: 5px;
	aspect-ratio: 87 / 110;
}
.cat-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--ion-color-dark-tint);
	line-height: 2;
	padding-top: 5px;
}
@media only screen and (max-width: 992px) {
  .cat-title  {
    font-size: 15px;
  }
  .cat-description {
    font-size: 12.5px;
  }
}
@media only screen and (max-width: 576px) {
	.grid-container {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
		padding: 0px;
		grid-gap: 15px;;
	}
	.grid-item {
		padding: 17px;
	}
}
</style>