let dietChart = null;

document
	.getElementById("healthForm")
	.addEventListener("submit", async function (e) {
		e.preventDefault();

		const btn = document.getElementById("submitBtn");
		const resultCard = document.getElementById("resultCard");

		btn.innerHTML =
			'<i class="fa-solid fa-circle-notch fa-spin"></i> Analyzing...';
		btn.style.opacity = "0.7";
		btn.disabled = true;
		resultCard.classList.add("hidden");

		const formData = {
			preg: document.getElementById("preg").value,
			glucose: document.getElementById("glucose").value,
			bp: document.getElementById("bp").value,
			skin: document.getElementById("skin").value,
			insulin: document.getElementById("insulin").value,
			bmi: document.getElementById("bmi").value,
			pedigree: document.getElementById("pedigree").value,
			age: document.getElementById("age").value,
		};

		try {
			const response = await fetch("/predict", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(formData),
			});

			const data = await response.json();

			if (data.error) throw new Error(data.error);

			// Update Text
			const title = document.getElementById("resultTitle");
			const score = document.getElementById("confidenceScore");
			const iconBox = document.getElementById("resultIcon");

			title.innerText = data.result;
			score.innerText = data.confidence;

			// Styling
			resultCard.classList.remove("Healthy", "Diabetic");
			resultCard.classList.add(data.result);

			if (data.result === "Diabetic") {
				title.innerText = "High Risk Detected";
				iconBox.innerHTML =
					'<i class="fa-solid fa-triangle-exclamation"></i>';
			} else {
				title.innerText = "Low Risk - Healthy";
				iconBox.innerHTML = '<i class="fa-solid fa-shield-heart"></i>';
			}

			// Render Chart
			renderDietChart(data.result);
			resultCard.classList.remove("hidden");
		} catch (error) {
			console.error("Error:", error);
			alert("Analysis failed. Check console.");
		} finally {
			btn.innerHTML =
				'Analyze Patient Data <i class="fa-solid fa-arrow-right"></i>';
			btn.style.opacity = "1";
			btn.disabled = false;
		}
	});

function renderDietChart(status) {
	const ctx = document.getElementById("dietChart").getContext("2d");

	if (dietChart) dietChart.destroy();

	let chartLabels, chartData, chartColors;

	if (status === "Diabetic") {
		chartLabels = ["Veg", "Protein", "Carbs", "Fats"];
		chartData = [50, 25, 15, 10];
		chartColors = ["#4caf50", "#2196f3", "#ff9800", "#f44336"];
	} else {
		chartLabels = ["Fruits/Veg", "Protein", "Carbs", "Fats"];
		chartData = [35, 25, 30, 10];
		chartColors = ["#66bb6a", "#42a5f5", "#ffca28", "#8d6e63"];
	}

	dietChart = new Chart(ctx, {
		type: "doughnut",
		data: {
			labels: chartLabels,
			datasets: [
				{
					data: chartData,
					backgroundColor: chartColors,
					borderWidth: 0,
					hoverOffset: 4,
				},
			],
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			plugins: {
				legend: {
					position: "right",
					labels: {
						color: "white",
						font: { size: 10 },
						boxWidth: 10,
						padding: 8,
					},
				},
				title: { display: false },
			},
			layout: { padding: 0 },
		},
	});
}
