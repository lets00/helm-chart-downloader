#!/bin/bash

links_file="links_download.txt"

download_directory="./downloads_bkp"
manifests_directory="./manifests"

mkdir -p "$download_directory"
mkdir -p "$manifests_directory"

while IFS= read -r link; do
    if [ -n "$link" ]; then
        filename=$(basename "$link")
        chart_name="${filename%.tar.gz}"
        chart_path="$download_directory/$filename"
        
        echo "Downloading $link..."
        wget -P "$download_directory" --tries=1 "$link"
        
        if [ $? -eq 0 ]; then
            echo "$link has download successfully."

            temp_dir=$(mktemp -d)
            
            tar -xzf "$chart_path" -C "$temp_dir"
            
            chart_dir=$(find "$temp_dir" -mindepth 1 -maxdepth 1 -type d)
            
            if [ $(echo "$chart_dir" | wc -l) -ne 1 ]; then
                echo "Error: incorrect chart dir."
                exit 1
            fi
            
            # Gerar os manifestos do Kubernetes usando helm template
            manifest_file="$manifests_directory/$chart_name-manifest.yaml"
            helm template my-release "$chart_dir" > "$manifest_file"
            
            if [ $? -eq 0 ]; then
                echo "Kubernetes Manifest generated in $manifest_file."
            else
                echo "Error to generate Kubernetes Manifesto: $chart_name."
            fi

            rm -rf "$temp_dir"
        else
            echo "Error to download $link."
        fi
    fi
done < "$links_file"
