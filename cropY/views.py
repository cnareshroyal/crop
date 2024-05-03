import os
import pickle
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    if request.method == 'POST':
        # Form submitted, process data
        state = request.POST.get('state')
        season = request.POST.get('season')
        file_path = os.path.join(os.path.dirname(__file__), 'multiple_objects.pkl')
        try:
            with open(file_path, 'rb') as f:
                model = pickle.load(f)
                decoded_mapping_state = pickle.load(f)
                decoded_mapping_season = pickle.load(f)
                X = pickle.load(f)
                decoded_mapping_crop = pickle.load(f)
        except FileNotFoundError:
            return HttpResponse("Pickle file not found.")
        
        state = decoded_mapping_state.get(state)
        season = decoded_mapping_season.get(season)
        if state is None or season is None:
            return HttpResponse("Invalid state or season.")
        
        result = []
        conditions = (X['State'] == state) & (X['Season'] == season)
        filtered_data = X[conditions].drop_duplicates()
        yields = list(model.predict(filtered_data))
        for i, j in zip(filtered_data.itertuples(), yields):
            result.append([state, season, i[3], j])
        sorted_list = sorted(result, key=lambda x: x[3])
        final_list = sorted_list[-5:]
        top_crops = [decoded_mapping_crop.get(item[2]) for item in final_list]
        context = {'top_crops': top_crops}
        return render(request, 'index.html', context)
    
    return render(request, 'index.html')
